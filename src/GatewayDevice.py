import docker, requests, time, json
from flask import request
from flask_restful import Resource, reqparse, fields, marshal

from Auth import auth
from configReader import ConfigReader

gateway_device_list = []

gateway_device_fields = {
    'gateway_device_id': fields.String,
    'docker_image': fields.String,
    'firmware_version': fields.String,
    'mac': fields.String,
    'agent_type': fields.String,
    'gateway_properties': fields.String,
    'container_port': fields.Integer
}


class GatewayDevices(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('container_port', type=int, required=True,
                                   help='No container port provided', location='json')
        self.reqparse.add_argument('mac', type=str, required=True,
                                   help='No gateway device mac provided', location='json')
        self.reqparse.add_argument('firmware_version', type=str, required=True,
                                   help='No firmware version provided', location='json')
        self.reqparse.add_argument('docker_image', type=str, required=True,
                                   help='No docker image provided', location='json')
        self.reqparse.add_argument('agent_type', type=str, required=True,
                                   help='No agent type provided', location='json')
        super(GatewayDevices, self).__init__()

    def get(self):

        return {'GatewayDevices': [marshal(gateway_device, gateway_device_fields)
                                   for gateway_device in gateway_device_list]}

    def post(self):

        is_test_controller = ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController')

        args = self.reqparse.parse_args()
        container_host_port = ConfigReader.read_config_value('INSTANCETYPE', 'ContainerHostPort')
        container_local_port = args['container_port']

        gateway_device = {
            'gateway_device_id': args['docker_image'] + '_' + str(container_local_port),
            'mac': args['mac'],
            'docker_image': args['docker_image'],
            'firmware_version': args['firmware_version'],
            'agent_type': args['agent_type'],
            'container_port': container_local_port
        }

        if is_test_controller == 'True':

            client = docker.from_env()

            client.containers.run(args['docker_image'],
                                  detach=True,
                                  name=args['docker_image'] + '_' + str(container_local_port),
                                  ports={str(container_host_port) + '/tcp': int(container_local_port)}
                                  )

            #give the container a chance to start before calling it
            time.sleep(3)

            url = ConfigReader.read_config_value('INSTANCETYPE', 'APIControllerUri') + ':' \
                  + str(container_local_port) \
                  + '/gatewaydevices'

            response = requests.post(url, data=json.dumps(gateway_device), headers=request.headers)

            #add the gateway to this controller's list of gateway\containers
            gateway_device_list.append(gateway_device)

            return response.json(), 201

        else:

            gateway_device_list.append(gateway_device)

            return {'GatewayDevice': marshal(gateway_device, gateway_device_fields)}, 201

    def delete(self):

        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') != 'True':
            # Allow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        client = docker.from_env()

        if client:
            containers = client.containers.list()

        for container in containers:
            container.stop()
            container.remove()

        gateway_device_list.clear()

        return {'result': True}


class GatewayDevice(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gateway_properties', type=str, required=True,
                                   help='No gateway properties provided', location='json')
        super(GatewayDevice, self).__init__()

    def get(self, gateway_device_id):

        return {'GatewayDevices': [marshal(gateway_device, gateway_device_fields)
                                   for gateway_device in gateway_device_list
                                   if gateway_device['gateway_device_id'] == gateway_device_id]}

    def delete(self, gateway_device_id):

        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') != 'True':
            # Allow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        client = docker.from_env()

        if client:
            container = client.containers.get(gateway_device_id)

        if container:
            container.stop()
            container.remove()

        gateway_device = [gateway_device for gateway_device in gateway_device_list
                          if gateway_device['gateway_device_id'] == gateway_device_id]

        if gateway_device:
            gateway_device_list.remove(gateway_device[0])

        return {'result': True}

    def put(self, gateway_device_id):

        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') == 'True':
            #Disallow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        self.reqparse.parse_args()

        new_gateway_properties = request.json['gateway_properties']

        #TODO pass gateway params off to XMPP Component

        gateway_device = [gateway_device for gateway_device in gateway_device_list
                          if gateway_device['gateway_device_id'] == gateway_device_id]

        if not gateway_device:
            abort(404)

        gateway_device = gateway_device[0]
        old_gateway_properties = (gateway_device['gateway_properties'])

        for key, value in new_gateway_properties.items():
            old_gateway_properties[key] = value

        return {'GatewayDevice': marshal(gateway_device, gateway_device_fields)}

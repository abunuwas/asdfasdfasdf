from flask import abort, request
from flask_restful import Resource, reqparse, fields, marshal

from src.Auth import auth
from src.configReader import ConfigReader

gateway_device_list = [
    {
        'gateway_device_id': '1',
        'docker_image': u'cameraAgent_132',
        'firmware_version': u'1.5.2',
        'mac': 'FF987654321E',
        'agent_type': 'EA2',
        'container_url': '',
        'gateway_properties': {}

    },
    {
        'gateway_device_id': '2',
        'docker_image': u'ensoAgent_243',
        'firmware_version': u'3.6.1',
        'mac': 'AA123456789B',
        'agent_type': 'EA3',
        'container_url': '',
        'gateway_properties': {}
    }
]

gateway_device_fields = {
    'gateway_device_id': fields.String,
    'docker_image': fields.String,
    'firmware_version': fields.String,
    'mac': fields.String,
    'agent_type': fields.String,
    'gateway_properties': fields.String,
    'container_url': fields.String
}


class GatewayDevices(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gateway_device_id', type=str, required=True,
                                   help='No gateway device id provided', location='json')
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

        #TODO return gateways with properties

        return {'GatewayDevices': [marshal(gateway_device, gateway_device_fields)
                                   for gateway_device in gateway_device_list]}

    def post(self):

        if ConfigReader.read_config_value('application-config', 'TestAPIController') != 'True':
            # Allow if is TestAPIController Config
            abort(400)

        args = self.reqparse.parse_args()

        #TODO Create container from docker image and return hostname of the container uri so
        #TODO that API can be accessed directly from JMETER

        gateway_device = {
            'gateway_device_id': args['gateway_device_id'],
            'mac': args['mac'],
            'docker_image': args['docker_image'],
            'firmware_version': args['firmware_version'],
            'agent_type': args['agent_type']
        }
        gateway_device_list.append(gateway_device)
        return {'GatewayDevice': marshal(gateway_device, gateway_device_fields)}, 201


class GatewayDevice(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gateway_properties', type=str, required=True,
                                   help='No gateway properties provided', location='json')
        super(GatewayDevice, self).__init__()

    def get(self, gateway_device_id):

        # TODO return gateway and properties

        return {'GatewayDevices': [marshal(gateway_device, gateway_device_fields)
                                   for gateway_device in gateway_device_list
                                   if gateway_device['gateway_device_id'] == gateway_device_id]}

    def delete(self, gateway_device_id):

        if ConfigReader.read_config_value('application-config', 'TestAPIController') != 'True':
            # Allow if is TestAPIController Config
            abort(400)

        #TODO tear down the container
        gateway_device = [gateway_device for gateway_device in gateway_device_list
                          if gateway_device['gateway_device_id'] == gateway_device_id]

        if not gateway_device:
            abort(404)

        gateway_device_list.remove(gateway_device[0])
        return {'result': True}

    def put(self, gateway_device_id):

        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            #Disallow if is TestAPIController Config
            abort(400)

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

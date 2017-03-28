import docker
import requests
import time
import json
import subprocess

from flask import request, abort
from flask_restful import Resource, reqparse, fields, marshal

from auth import auth
from config_reader import ConfigReader
import api_decorators

_gateway_device_list = []

_gateway_device_fields = {
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
    """Used for creating new containers, deleting all containers and retrieving a list of running containers"""

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
        """
        Gets the list of existing containers
        :return: List of existing containers
        """

        return {'GatewayDevices': [marshal(gateway_device, _gateway_device_fields)
                                   for gateway_device in _gateway_device_list]}

    def post(self):
        """
        Creates a new container for a gateway. When called as API Controller the container is created and started.  As
        soon as the state of the container is 'healthy' then this method is called on the API within the container to
        setup the container's gateway properties.
        :return: The created gateway device
        """

        is_test_controller = ConfigReader.read_config_value('INSTANCETYPE', 'IsTestAPIController')

        args = self.reqparse.parse_args()
        container_host_port = ConfigReader.read_config_value('INSTANCETYPE', 'ContainerHostPort')
        container_local_port = args['container_port']
        container_name = args['docker_image'] + '_' + str(container_local_port)

        gateway_device = {
            'gateway_device_id': container_name,
            'mac': args['mac'],
            'docker_image': args['docker_image'],
            'firmware_version': args['firmware_version'],
            'agent_type': args['agent_type'],
            'container_port': container_local_port,
            'gateway_properties': {}
        }

        if is_test_controller == 'True':

            client = docker.from_env()

            client.containers.run(args['docker_image'],
                                  detach=True,
                                  name=container_name,
                                  ports={str(container_host_port) + '/tcp': int(container_local_port)}
                                  )

            # Give the container a chance to start before calling it
            while subprocess.check_output(
                    ["/usr/bin/docker", "inspect",  "-f",
                     "{{.State.Health.Status}}", container_name]) != b"healthy\n":
                time.sleep(1)

            url = (ConfigReader.read_config_value('INSTANCETYPE', 'APIControllerUri')
                   + ':' + str(container_local_port) + '/gatewaydevices')

            response = requests.post(url, data=json.dumps(gateway_device), headers=request.headers)

            # Add the gateway to this controller's list of gateway\containers
            _gateway_device_list.append(gateway_device)

            return response.json(), 201

        else:

            _gateway_device_list.append(gateway_device)

            return {'GatewayDevice': marshal(gateway_device, _gateway_device_fields)}, 201

    @api_decorators.api_controller_type_verifier('True')
    def delete(self):
        """
        Stops and removes all existing containers, clears the gateway device list
        :return: True
        """

        client = docker.from_env()

        if client:
            containers = client.containers.list()

        for container in containers:
            container.stop()
            container.remove()

        _gateway_device_list.clear()

        return {'result': True}


class GatewayDevice(Resource):
    decorators = [auth.login_required]
    """Used to update, return and delete single gateway instances"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('gateway_properties', type=str, required=True,
                                   help='No gateway properties provided', location='json')
        super(GatewayDevice, self).__init__()

    def get(self, gateway_device_id):
        """
        Retrieves a gateway device based on the gateway device id
        :param gateway_device_id: Unique name for the container
        :return: A gateway device
        """

        return {'GatewayDevices': [marshal(gateway_device, _gateway_device_fields)
                                   for gateway_device in _gateway_device_list
                                   if gateway_device['gateway_device_id'] == gateway_device_id]}

    @api_decorators.api_controller_type_verifier('True')
    def delete(self, gateway_device_id):
        """
        Stops and removes an existing containers and deletes a single gateway device from the list of existing gateways
        :param gateway_device_id: Unique name for the container
        :return: True
        """

        client = docker.from_env()

        if client:
            container = client.containers.get(gateway_device_id)

        if container:
            container.stop()
            container.remove()

        gateway_device = [gateway_device for gateway_device in _gateway_device_list
                          if gateway_device['gateway_device_id'] == gateway_device_id]

        if gateway_device:
            _gateway_device_list.remove(gateway_device[0])

        return {'result': True}

    @api_decorators.api_controller_type_verifier('False')
    def put(self, gateway_device_id):
        """
        Updates a gateway devices's properties, can only be called for API running in a container
        :param gateway_device_id: Unique identifier for the container
        :return: The updated gateway device
        """

        self.reqparse.parse_args()

        new_gateway_properties = request.json['gateway_properties']

        # TODO pass gateway params off to XMPP Component

        gateway_device = [gateway_device for gateway_device in _gateway_device_list
                          if gateway_device['gateway_device_id'] == gateway_device_id]

        if not gateway_device:
            abort(404)

        gateway_device = gateway_device[0]

        old_gateway_properties = gateway_device['gateway_properties']

        for key, value in new_gateway_properties.items():
            old_gateway_properties[key] = value

        return {'GatewayDevice': marshal(gateway_device, _gateway_device_fields)}

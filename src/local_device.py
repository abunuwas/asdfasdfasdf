from flask import request, abort
from flask_restful import Resource, reqparse, fields, marshal

from auth import auth
import api_decorators

_local_device_list = []

_local_device_fields = {
    'local_device_id': fields.String,
    'mac': fields.String,
    'gateway_device_id': fields.String,
    'local_device_properties': fields.String,
    'template_name': fields.String
}


class LocalDevices(Resource):
    decorators = [auth.login_required]
    """Represents a list of sensors added to the gateway device within a container"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mac', type=str, required=True,
                                   help='No mac provided', location='json')
        self.reqparse.add_argument('local_device_id', type=str, required=True,
                                   help='No local device id provided', location='json')
        self.reqparse.add_argument('template_name', type=str, required=True,
                                   help='No device template provided', location='json')
        super(LocalDevices, self).__init__()

    @api_decorators.api_controller_type_verifier('False')
    def get(self, gateway_device_id):
        """
        Retrieves a list of sensors paired to the gateway
        :param gateway_device_id: Unique identifier for the container
        :return: List of local devices
        """

        return {'LocalDevices': [marshal(local_device, _local_device_fields) for local_device in _local_device_list
                                 if local_device['gateway_device_id'] == gateway_device_id]}

    @api_decorators.api_controller_type_verifier('False')
    def post(self, gateway_device_id):
        """
        Creates a new local device on an existing gateway
        :param gateway_device_id: Unique identifier for the container
        :return: The created local device
        """

        # TODO create local device
        args = self.reqparse.parse_args()

        local_device = request.json
        local_device['gateway_device_id'] = gateway_device_id
        local_device['mac'] = args['mac']
        local_device['local_device_id'] = args['local_device_id']
        local_device['template_name'] = args['template_name']

        if request.json['local_device_properties']:
            local_device['local_device_properties'] = request.json['local_device_properties']
        else:
            local_device['local_device_properties'] = {}

        _local_device_list.append(local_device)

        return {'LocalDevices': marshal(local_device, _local_device_fields)}, 201


class LocalDevice(Resource):
    decorators = [auth.login_required]
    """Represents a single sensor paired to a gateway"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('local_device_properties', type=str, required=True,
                                   help='No local device properties provided', location='json')
        super(LocalDevice, self).__init__()

    @api_decorators.api_controller_type_verifier('False')
    def get(self, gateway_device_id, local_device_id):
        """
        Returns a specific local device paired to a gateway
        :param gateway_device_id: Unique identifier for a container
        :param local_device_id: Local device identifier
        :return: A local device
        """

        return {'LocalDevice': [marshal(local_device, _local_device_fields) for local_device in _local_device_list
                                if local_device['gateway_device_id'] == gateway_device_id
                                and local_device['local_device_id'] == local_device_id]}

    @api_decorators.api_controller_type_verifier('False')
    def put(self, gateway_device_id, local_device_id):
        """
        Updates the properties of a local device on a gateway
        :param gateway_device_id: Unique identifier for the container
        :param local_device_id: Local device identifier to be updated
        :return: The updated local device
        """

        self.reqparse.parse_args()

        # TODO update local device properties
        new_props = request.json['local_device_properties']

        local_device = [local_device for local_device in _local_device_list
                        if local_device['gateway_device_id'] == gateway_device_id
                        and local_device['local_device_id'] == local_device_id]

        if not local_device:
            abort(404)

        local_device = local_device[0]
        old_props = (local_device['local_device_properties'])

        for key, value in new_props.items():
            old_props[key] = value

        return {'LocalDevice': marshal(local_device, _local_device_fields)}

    @api_decorators.api_controller_type_verifier('False')
    def delete(self, gateway_device_id, local_device_id):
        """
        Removes a local device from the local devices list
        :param gateway_device_id: Unique identifier for the container
        :param local_device_id: Local device identifier to be deleted
        :return: True
        """

        # TODO remove local device
        local_device = [local_device for local_device in _local_device_list
                        if local_device['gateway_device_id'] == gateway_device_id
                        and local_device['local_device_id'] == local_device_id]

        if not local_device:
            abort(404)

        _local_device_list.remove(local_device[0])

        return {'result': True}

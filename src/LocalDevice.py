from flask import abort, request
from flask_restful import Resource, reqparse, fields, marshal

from src.Auth import auth
from src.configReader import ConfigReader

local_device_list = [
    {
        'local_device_id': '1',
        'gateway_device_id': '1',
        'local_device_properties':
        {
            'prop_name1': 'prop_value1',
            'prop_name2': 'prop_value2'
        }
    },
    {
        'local_device_id': '2',
        'gateway_device_id': '1',
        'local_device_properties':
        {
            'prop_name1': 'prop_value1',
            'prop_name2': 'prop_value2'
        }
    }
]

local_device_fields = {
    'local_device_id': fields.String,
    'gateway_device_id': fields.String,
    'local_device_properties': fields.String
}


class LocalDevices(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('device_id', type=str, required=True,
                                   help='No local device id provided', location='json')
        self.reqparse.add_argument('template', type=str, required=True,
                                   help='No device template provided', location='json')
        super(LocalDevices, self).__init__()

    def get(self, gateway_device_id):

        # TODO return all local devices for a gateway
        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            abort(400)

        return {'LocalDevices': [marshal(local_device, local_device_fields) for local_device in local_device_list
                                 if local_device['gateway_device_id'] == gateway_device_id]}

    def post(self, gateway_device_id):

        # TODO create local device
        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            abort(400)

        args = self.reqparse.parse_args()

        local_device = request.json
        local_device['gateway_device_id'] = gateway_device_id
        local_device['local_device_id'] = args['device_id']
        local_device['template_name'] = args['template']
        local_device['local_device_properties'] = request.json['local_device_properties']

        local_device_list.append(local_device)

        return {'LocalDevices': marshal(local_device, local_device_fields)}, 201


class LocalDevice(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('local_device_properties', type=str, required=True,
                                   help='No local device properties provided', location='json')
        super(LocalDevice, self).__init__()

    def get(self, gateway_device_id, local_device_id):

        # TODO return local device with properties
        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            abort(400)

        return {'LocalDevice': [marshal(local_device, local_device_fields) for local_device in local_device_list
                                if local_device['gateway_device_id'] == gateway_device_id
                                and local_device['local_device_id'] == local_device_id]}

    def put(self, gateway_device_id, local_device_id):

        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            abort(400)

        self.reqparse.parse_args()

        # TODO update local device properties
        new_props = request.json['local_device_properties']

        local_device = [local_device for local_device in local_device_list
                        if local_device['gateway_device_id'] == gateway_device_id
                        and local_device['local_device_id'] == local_device_id]

        if not local_device:
            abort(404)

        local_device = local_device[0]
        old_props = (local_device['local_device_properties'])

        for key, value in new_props.items():
            old_props[key] = value

        return {'LocalDevice': marshal(local_device, local_device_fields)}

    def delete(self, gateway_device_id, local_device_id):

        if ConfigReader.read_config_value('application-config', 'TestAPIController') == 'True':
            # Allow if is TestAPIController Config
            abort(400)

        # TODO remove local device
        local_device = [local_device for local_device in local_device_list
                        if local_device['gateway_device_id'] == gateway_device_id
                        and local_device['local_device_id'] == local_device_id]

        if not local_device:
            abort(404)

        local_device_list.remove(local_device[0])

        return {'result': True}

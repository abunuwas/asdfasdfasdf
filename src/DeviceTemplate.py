from flask import request
from flask_restful import Resource, reqparse, fields, marshal

from Auth import auth
from configReader import ConfigReader

device_template_list = []

device_template_fields = {
    'gateway_device_id': fields.String,
    'mac': fields.String,
    'template_name': fields.String,
    'template_properties': fields.String
}


class DeviceTemplates(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mac', type=str, required=True,
                                   help='No gateway device mac provided', location='json')
        super(DeviceTemplates, self).__init__()

    def get(self):

        # TODO return all device templates
        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        return {'DeviceTemplates': [marshal(device_template, device_template_fields)
                                    for device_template in device_template_list]}

    def post(self, gateway_device_id, template_name):

        # TODO create new device template
        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        args = self.reqparse.parse_args()

        device_template = request.json
        device_template['template_name'] = template_name
        device_template['gateway_device_id'] = gateway_device_id
        device_template['mac'] = args['mac']
        device_template['template_properties'] = request.json['template_properties']

        device_template_list.append(device_template)

        return {'DeviceTemplates': marshal(device_template, device_template_fields)}, 201


class DeviceTemplate(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('template_properties', type=str, required=True,
                                   help='No template properties provided', location='json')
        super(DeviceTemplate, self).__init__()

    def put(self, gateway_device_id, template_name):

        # TODO update template properties
        if ConfigReader.read_config_value('INSTANCETYPE', 'TestAPIController') == 'True':
            # Disallow if is TestAPIController Config
            return 'Method not supported for controller type', 400

        self.reqparse.parse_args()

        new_props = request.json['template_properties']

        device_template = [device_template for device_template in device_template_list
                           if device_template['gateway_device_id'] == gateway_device_id
                           and device_template['template_name'] == template_name]

        if not device_template:
            abort(404)

        device_template = device_template[0]
        old_props = (device_template['template_properties'])

        for key, value in new_props.items():
            old_props[key] = value

        return {'DeviceTemplate': marshal(device_template, device_template_fields)}

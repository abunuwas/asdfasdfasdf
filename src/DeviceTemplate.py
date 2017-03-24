from flask import request, abort
from flask_restful import Resource, reqparse, fields, marshal

from Auth import auth

import Decorators

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

    @Decorators.api_controller_type_verifier('False')
    def get(self):

        # TODO return all device templates
        return {'DeviceTemplates': [marshal(device_template, device_template_fields)
                                    for device_template in device_template_list]}

    @Decorators.api_controller_type_verifier('False')
    def post(self, gateway_device_id, template_name):

        # TODO create new device template
        args = self.reqparse.parse_args()

        device_template = request.json
        device_template['template_name'] = template_name
        device_template['gateway_device_id'] = gateway_device_id
        device_template['mac'] = args['mac']

        if request.json['template_properties']:
            device_template['template_properties'] = request.json['template_properties']
        else:
            device_template['template_properties'] = {}

        device_template_list.append(device_template)

        return {'DeviceTemplates': marshal(device_template, device_template_fields)}, 201


class DeviceTemplate(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('template_properties', type=str, required=True,
                                   help='No template properties provided', location='json')
        super(DeviceTemplate, self).__init__()

    @Decorators.api_controller_type_verifier('False')
    def put(self, gateway_device_id, template_name):

        # TODO update template properties
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

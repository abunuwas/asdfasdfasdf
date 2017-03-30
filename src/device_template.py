from flask import request, abort
from flask_restful import Resource, reqparse, fields, marshal

from auth import auth
import api_decorators
from src import _device_template_list, _device_template_fields



class DeviceTemplates(Resource):
    decorators = [auth.login_required]
    """Used for creating and returning local device templates within the container"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('mac', type=str, required=True,
                                   help='No gateway device mac provided', location='json')
        super(DeviceTemplates, self).__init__()

    @api_decorators.api_controller_type_verifier('False')
    def get(self):
        """
        Get a list of device templates within the container
        :return: List of device templates
        """
        return {'DeviceTemplates': [marshal(device_template, _device_template_fields)
                                    for device_template in _device_template_list]}

    @api_decorators.api_controller_type_verifier('False')
    def post(self, gateway_device_id, template_name):
        """
        Creates a device template within the container
        :param gateway_device_id: Unique name for the container
        :param template_name: Description for the template
        :return: Created device template
        """
        args = self.reqparse.parse_args()
        device_template = request.json
        device_template['template_name'] = template_name
        device_template['gateway_device_id'] = gateway_device_id
        device_template['mac'] = args['mac']

        if request.json['template_properties']:
            device_template['template_properties'] = request.json['template_properties']
        else:
            device_template['template_properties'] = {}

        _device_template_list.append(device_template)

        return {'DeviceTemplates': marshal(device_template, _device_template_fields)}, 201


class DeviceTemplate(Resource):
    decorators = [auth.login_required]
    """Used for retrieving and updating individual device templates"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('template_properties', type=str, required=True,
                                   help='No template properties provided', location='json')
        super(DeviceTemplate, self).__init__()

    @api_decorators.api_controller_type_verifier('False')
    def put(self, gateway_device_id, template_name):
        """
        Updates the specified device template
        :param gateway_device_id: Unique identifier for the container
        :param template_name: Name of the template being updated
        :return: The updated device template
        """

        self.reqparse.parse_args()

        new_props = request.json['template_properties']

        device_template = [device_template for device_template in _device_template_list
                           if device_template['gateway_device_id'] == gateway_device_id
                           and device_template['template_name'] == template_name]

        if not device_template:
            abort(404)

        device_template = device_template[0]
        old_props = (device_template['template_properties'])

        for key, value in new_props.items():
            old_props[key] = value

        return {'DeviceTemplate': marshal(device_template, _device_template_fields)}

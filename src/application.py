import logging
import sys

from flask import Flask, jsonify, make_response
from flask_restful import Api

from src.GatewayDevice import GatewayDevices, GatewayDevice
from src.DeviceTemplate import DeviceTemplates, DeviceTemplate
from src.LocalDevice import LocalDevices, LocalDevice

app = Flask(__name__, static_url_path="")
api = Api(app)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#gateway devices & params end points
api.add_resource(GatewayDevices, '/gatewaydevices', endpoint='gatewaydevices')
api.add_resource(GatewayDevice, '/gatewaydevices/<string:gateway_device_id>', endpoint='gatewaydevice')

#device template end point
api.add_resource(DeviceTemplates, '/devicetemplates/<string:gateway_device_id>/<string:template_name>',
                 endpoint='devicetemplates')
api.add_resource(DeviceTemplate, '/devicetemplates/<string:gateway_device_id>/<string:template_name>',
                 endpoint='devicetemplate')

#local device end points
api.add_resource(LocalDevices, '/localdevices/<string:gateway_device_id>', endpoint='localdevices')
api.add_resource(LocalDevice, '/localdevices/<string:gateway_device_id>/<string:local_device_id>',
                 endpoint='localdevice')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

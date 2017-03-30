from configparser import ConfigParser
import logging
import os
import sys

from flask_restful import fields

from xmpp.component import Component

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logging.debug('haaaaaaaaaaaaa')

this_dir = os.path.abspath(os.path.dirname(__file__))
config_dir = os.path.join(this_dir, '..', 'config')
config_file = os.path.join(config_dir, 'application.config')

parser = ConfigParser()
parser.read(config_file)
logging.debug(parser)
instance_type = parser['INSTANCETYPE']

xmpp_component = None

def incoming(_, stanza):
    logging.log(stanza)

_device_template_list = []

_device_template_fields = {
    'gateway_device_id': fields.String,
    'mac': fields.String,
    'template_name': fields.String,
    'template_properties': fields.String
}

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

if not instance_type.getboolean('IsTestAPIController'):
    from xml.etree import ElementTree as ET
    import datetime

    presence = ET.fromstring("""<presence from="4419b625e173@use-xmpp-01/camera" to="mzcameraxmppapp@use-xmpp-01/xmppadmin" lang="en" xmlns="jabber:component" />""")
    xmpp_component = Component(None, None, None, None, None, None, None)
    xmpp_component._start_thread('event_thread_%s' % 5, xmpp_component._event_runner)
    xmpp_component.incoming = incoming
    xmpp_component._XMLStream__spawn_event(presence)
    gateway = {
        'gateway_device_id': 'asdf1234',
        'gateway_properties': {
            'firmware_version': '1.2.3'
        }
    }
    _gateway_device_list.append(gateway)
    heat_alarm_template = {
        'template_name': 'heatAlarmTemplate',
        'gateway_device_id': 'wisafe.HeatAlarm.1234',
        'mac': 'asdf1234',
        'template_properties': {
            'sequence': '43',
            'status': '0',
            'id': '1234',
            'alert': 'tested.0x01',
            'timestamp': datetime.datetime.utcnow(),
            'code': '43'
        }
    }
    #_device_template_list.append(heat_alarm_template)



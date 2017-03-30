import datetime
import json
import time

import requests


ip = 'http://167.165.110.29:5002/'
headers = {'Content-Type': 'application/json'}

template_data = {
    'template_name': 'heatAlarmTemplate',
    'gateway_device_id': 'wisafe.HeatAlarm.1234',
    'mac': 'asdf1234',
    'template_properties': {
        'sequence': '43',
        'status': '0',
        'id': '1234',
        'alert': 'tested.0x01',
        'timestamp': time.time(),
        'code': '43'
    }
}

r = requests.post(ip+'devicetemplates/asdf1234/heatAlarmTemplate', data=json.dumps(template_data), auth=('username', 'password'), headers=headers)

print(r.status_code)
print(r.json())

time.sleep(1)

local_device_data = {
    "mac": 'asdf1234',
    'local_device_id': 'wisafe.HeatAlarm.1234',
    'template_name': 'heatAlarmTemplate',
    'local_device_properties': {}
}

r = requests.post(ip+'localdevices/asdf1234', data=json.dumps(local_device_data), auth=('username', 'password'), headers=headers)

print(r.status_code)
print(r.json())

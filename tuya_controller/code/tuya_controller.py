import pytuya
import json
import requests
from flask import Flask
from flask_restful import Resource, Api


tuya_controller = Flask(__name__)
api = Api(tuya_controller)

class TuyaDevices(Resource):

    # GET request to list all devices in the device list
    def get(self):
        with open('/code/devices.json') as json_file:
            device_list = json.load(json_file)

        return {'message': 'Success', 'data': device_list}, 200

class Outlet(Resource):

    # Initialize outlet resource data
    def __init__(self):
        with open('/code/devices.json') as json_file:
            self.device_list = json.load(json_file)

    def get(self, identifier):
        device_data = {}
        for device in self.device_list:
            if device['device_id'] == identifier:
                device_data = device

        if not device_data:
            return {'message': 'Device not found', 'data': {}}, 404
        else:
            return {'message': 'Device found', 'data': device_data}, 200

class Outlet_Status(Resource):

    def get(self, identifier):
        url = 'http://localhost:5001/outlet/' + identifier
        response = requests.request("GET", url).json()
        device_data = response['data']
        device_id = device_data['device_id']
        ip = device_data['ip']
        local_key = device_data['local_key']

        d = pytuya.OutletDevice(device_id, ip, local_key)
        data = d.status()
        state = data['dps']['1']

        return {'message': 'Success', 'data': {'state' : state}}, 200

class Outlet_Switch(Resource):

    def post(self, identifier):
        url = 'http://localhost:5001/outlet/' + identifier
        response = requests.request("GET", url).json()
        device_data = response['data']
        device_id = device_data['device_id']
        ip = device_data['ip']
        local_key = device_data['local_key']

        d = pytuya.OutletDevice(device_id, ip, local_key)
        data = d.status()
        state = data['dps']['1']
        data = d.set_status(not state)

        return {'message': 'Success', 'data': {'state' : not state}}, 200

api.add_resource(TuyaDevices, '/devices')
api.add_resource(Outlet, '/outlet/<string:identifier>')
api.add_resource(Outlet_Status, '/outlet/<string:identifier>/status')
api.add_resource(Outlet_Switch, '/outlet/<string:identifier>/switch')

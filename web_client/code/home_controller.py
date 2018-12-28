from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api, reqparse
import requests
from datetime import datetime
import json
import os


home_controller = Flask(__name__, static_url_path="", static_folder="static")
api = Api(home_controller)


# Main app route
@home_controller.route("/")
def main():

    title = "Home Controller"

    server_ip = os.environ['SERVERIP']

    # GET door status string from status API
    url = server_ip + ':5000/garage'
    response = requests.request("GET", url).json()
    door_state = response['data']['state']
    last_time = str(response['data']['last_time'])

    # Calculate time since garage door has moved
    last_time = datetime.strptime(last_time[:-2]+'Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    now = datetime.utcnow()
    diff = now - last_time
    seconds = diff.total_seconds()
    if seconds < 60:
        elapsed = str(round(seconds)) + ' sec'
    elif seconds >= 60 and seconds < 3600:
        elapsed = str(round(seconds / 60)) + ' min'
    elif seconds >= 3600 and seconds < 86400:
        elapsed = str(round(seconds / 60 / 60)) + ' hours'
    else:
        elapsed = str(round(seconds / 60 / 60 / 24)) + ' days'

    # GET washing machine status string from status API
    url = server_ip + ':5002/dishwasher'
    try:
        response = requests.request("GET", url).json()
        dishwasher_state = response['data']['clean']
    except:
        dishwasher_state = "Error"
        print('Dishwasher Read Error')

    if dishwasher_state == True:
        dishwasher_state = "Clean"
    elif dishwasher_state == False:
        dishwasher_state = "Dirty"
    else:
        dishwasher_state = "Error"

    # GET weather data
    url = server_ip + ':5003/weather'
    response = requests.request("GET", url).json()
    weather = response['data']

    # GET request to get status of all Tuya devices
    url = server_ip + ':5001/devices'
    response = requests.request("GET", url).json()
    device_list = response['data']
    tuya_states = []
    for device in device_list:
        device_id = device['device_id']
        url = server_ip + ':5001/outlet/' + device_id + '/status'
        try:
            response = requests.request("GET", url).json()
            device_state = response['data']['state']
        except:
            device_state = 'Error'
            print(device_id, '- Error')
        if device_state == True:
            tuya_states.append('On')
        elif device_state == 'Error':
            tuya_states.append('-')
        else:
            tuya_states.append('Off')

    templateData = {
        'title' : title,
        'server_ip' : server_ip,
        'door_state' : door_state,
        'door_time' : elapsed,
        'dishwasher_state' : dishwasher_state,
        'weather' : weather,
        'vanity_state' : tuya_states[0],
        'fireplace_state' : tuya_states[1],
        'small_tree_state' : tuya_states[2],
        'tree_state' : tuya_states[3],
        'lamp_state' : "On",
        }

    return render_template('home_controller.html', **templateData)

# Plots app route
@home_controller.route("/plots")
def plots():

    title = "Home Controller"

    server_ip = os.environ['SERVERIP']

    power_url = server_ip + ':5004/get_render?plot=1'
    gas_url = server_ip + ':5004/get_render?plot=2'
    water_url = server_ip + ':5004/get_render?plot=3'

    templateData = {
        'title' : title,
        'power_url' : power_url,
        'gas_url' : gas_url,
        'water_url' : water_url
        }

    return render_template('plot_page.html', **templateData)

# Media app route
@home_controller.route("/media")
def media():

    title = "Home Controller"

    templateData = {
        'title' : title
        }

    return render_template('media_page.html', **templateData)

# Camera app route
@home_controller.route("/cam")
def cam():

    title = "Home Controller"

    cam_ip = os.environ['CAMIP']
    cam_un = os.environ['CAMUSERNAME']
    cam_pw = os.environ['CAMPASSWORD']

    templateData = {
        'title' : title,
        'cam_ip' : cam_ip,
        'cam_un' : cam_un,
        'cam_pw' : cam_pw
        }

    return render_template('cam_page.html', **templateData)
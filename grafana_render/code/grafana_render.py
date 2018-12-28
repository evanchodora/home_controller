from flask import Flask, send_file, request
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit
from subprocess import call


# Initialize Flask app and API resource
grafana_render = Flask(__name__)

# Function to update images of Grafana plots
def get_renders():

    try:
        # Run script to get new renders
        call(["/code/render_grafana"])
    except:
        pass

# Schedule job to update data from API
scheduler = BackgroundScheduler(timezone='US/Eastern')
scheduler.add_job(func=get_renders, trigger="interval", minutes=15)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@grafana_render.route('/get_render')
def get_image():
    if request.args.get('plot') == '1':
        filename = 'power.png'
    elif request.args.get('plot') == '2':
        filename = 'gas.png'
    elif request.args.get('plot') == '3':
        filename = 'water.png'

    return send_file(filename, mimetype='image/png')

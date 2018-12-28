import pymyq
from flask_restful import Resource, Api
from flask import Flask


garage_controller = Flask(__name__)
api = Api(garage_controller)

# API resource for controlling and viewing garage door state
class Garage(Resource):

    # Initialize a Door object and login
    def __init__(self):
        self.door = pymyq.Door()

    # GET door current status
    def get(self):
        door_state = self.door.status()

        return {'message': 'Success', 'data': door_state}, 200

    # POST to change current door state
    def post(self):
        self.door.change_door_state()

        return {'message': 'Success', 'data': {"state": "Changing"}}, 200

# Add API resource locations
api.add_resource(Garage, '/garage')

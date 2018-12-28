import pickledb
from flask_restful import Resource, Api
from flask import Flask


dishwasher = Flask(__name__)
api = Api(dishwasher)

# API resource for controlling and viewing dishwasher state
class Clean_State(Resource):

    # Initialize by loading database
    def __init__(self):
        self.db = pickledb.load('/code/dishwasher.db', True)

    # GET dishwasher current status
    def get(self):
        state = self.db.get('clean')

        return {'message': 'Success', 'data': {'clean': state}}, 200

    # POST to change current dishwasher state
    def post(self):
        state = self.db.get('clean')
        self.db.set('clean', not state)

        return {'message': 'Success', 'data': {'clean': not state}}, 200

# Add API resource locations
api.add_resource(Clean_State, '/dishwasher')

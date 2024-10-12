from flask_restx import Resource, Namespace
import json

ns = Namespace("api")

@ns.route("/coords")
class CoordsResource(Resource):
    def get(self):
        # Open and read the coords JSON file
        with open('coords.json', 'r') as file:
            data = json.load(file)

        return {"coords": data}
import sqlite3
from flask import Flask, request
from flask import jsonify
from flask import request
from flask_restful import Api, Resource
from mybackend import Database

app = Flask(__name__)
api = Api(app)
# ?startlocation=<startlocation>&timeduration=<timeduration>&k=<k>
# @app.route('/', methods=['GET'])
# def get():
#     startlocation = request.params.require('startlocation').permit('startlocation')
#     timeduration = request.params.require('timeduration').permit('timeduration')
#     k = request.params.require('k').permit('k')
#     db = Database()
#     res = db.get_recommendation(startlocation, timeduration, k)
#     res_dct = {i: res[i] for i in range(0, len(res))}
#     return res_dct


class recommend(Resource):
    def get(self, location, minutes, places):
        """Creates a get api request - returns json of the locations that we recommend for the user"""
        db = Database()
        res = db.get_recommendation(location, minutes, places)
        res_dct = {i: res[i] for i in range(0, len(res))}
        return res_dct


# specify how the get url would look like.
api.add_resource(recommend, '/<string:location>/<int:minutes>/<int:places>')

if __name__ == '__main__':
    app.run(debug=True)

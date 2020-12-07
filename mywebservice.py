import sqlite3
from flask import Flask, request
from flask import jsonify
from flask import request
import json
from flask_restful import Api, Resource
from mybackend import Database

app = Flask(__name__)
api = Api(app)


@app.route('/')
def get():
    """Creates a get api request - returns json of the locations that we recommend for the user"""
    startlocation = request.args.get('startlocation')
    timeduration = request.args.get('timeduration')
    k = request.args.get('k')
    db = Database()
    try:
        res = db.get_recommendation(startlocation, timeduration, k)
        res = list(res['EndStationName'])
        json_string = json.dumps(res)
        return json_string
    except ValueError:
        return json.dumps("error: timeduration must be a number and k must be a integer number")




if __name__ == '__main__':
    app.run(debug=False)
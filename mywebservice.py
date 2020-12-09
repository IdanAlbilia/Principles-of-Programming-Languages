from flask import Flask
from flask import request
import json
from flask_restful import Api
from mybackend import Database

app = Flask(__name__)
api = Api(app)
"""This class is web service that communicates with the database"""


@app.route('/')
def get():
    """Creates a get api request - returns json of the locations that we recommend for the user"""
    start_location = request.args.get('startlocation')
    time_duration = request.args.get('timeduration')
    k = request.args.get('k')
    db = Database()
    try:
        res = db.get_recommendation(start_location, time_duration, k)
        res = list(res['EndStationName'])
        json_string = json.dumps(res)
        return json_string
    except ValueError:
        return json.dumps("error: timeduration and k must be a positive number ")


if __name__ == '__main__':
    app.run(debug=False)

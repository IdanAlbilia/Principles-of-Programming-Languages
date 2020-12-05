import sqlite3
from flask import Flask, request
from flask import jsonify
from flask import request
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
        # cant send list as json (unlike example in the assignment - only dict, tuple or string)
        res_dct = {i: res[i] for i in range(0, len(res))}
        # res_dct = [res[i] for i in range(0, len(res))]
        return res_dct
    except Exception as e:
        print(e)
        return {}


# another way to create a get request
# class recommend(Resource):
#     def get(self, startlocation, timeduration, k):
#         """Creates a get api request - returns json of the locations that we recommend for the user"""
#         db = Database()
#         try:
#             res = db.get_recommendation(startlocation, timeduration, k)
#             res_dct = [res[i] for i in range(0, len(res))]
#             return res_dct
#         except:
#             return []
# specify how the get url would look like.
# api.add_resource(recommend, '/<string:startlocation>/<int:timeduration>/<int:k>')

if __name__ == '__main__':
    app.run(debug=True)

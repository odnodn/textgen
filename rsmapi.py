#pip install flask flask-restful
# test : curl --header "Content-Type: application/json"   --request POST   --data '{"firstName":"and","lastName":"and"}'   http://localhost:5050/rs/validatenames


from flask import Flask,jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.routing import NotFound
import json


parser = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)

class Customer:

    def __init__(self, name='john', surname='smit') :
        self.firstName = name
        self.lastName = surname

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True,)

class Query(Resource):

    def options (self):
        return {'Allow' : 'POST' }, 200, \
               { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

    def get(self):
        return {'hello': 'world'}

    def put(self):
        return {'message':'request cancelled'}

    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        sn = ""
        pw = ""
        try:
            sn = int(json_data['serviceDetailsId'])
            if(sn < 1000): raise NotFound("No transaction found ")

        except:
           abort("Invalid transaction id")

        cust = Customer()
        print(cust)

        return ([{"serviceDetailsId" : sn, "customer": {'firstName': 'john', 'lastName':'shrill'}},])


        print("got "  + un)
        return []

class Amend(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        json_data = request.get_json(force=True)
        print(json_data)
        rn = json_data['comment']
        if(rn.startswith("j")):
            abort(400)
        return {'message':'request cancelled because of ' + rn}


api.add_resource(Query, '/rsm/mailforwardingandholdmail/query/service')
api.add_resource(Amend,'/rsm/mailforwardingandholdmail/2219/amendstatus/')

if __name__ == '__main__':
    app.run(debug=True, port=5026)
#pip install flask flask-restful
# test : curl --header "Content-Type: application/json"   --request POST   --data '{"firstName":"and","lastName":"and"}'   http://localhost:5050/rs/validatenames


from flask import Flask,jsonify, request
from flask_restful import Resource, Api, reqparse

parser = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):

    def options (self):
        return {'Allow' : 'POST' }, 200, \
               { 'Access-Control-Allow-Origin': '*', \
                 'Access-Control-Allow-Methods' : 'PUT,GET' }

    def get(self):
        return {'hello': 'world'}

    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        un = ""
        pw = ""
        try:
            un = json_data[0]['firstName']
            pw = json_data[0]['lastName']
        except:
            try:
                un = json_data[0]['businessName']
            except:
                return []

        #if(un  == '' and pw == ''):  un = json_data[0]['businessName']

        typeCd= "typeCd"

        if(un  == 'and' or pw == 'and'): return ([{typeCd : 2},])
        if( (un  == 'plumbing' or un =="tech") or (pw  == 'plumbing' or pw =="tech")  ):
            return ([{typeCd : 1},])

        if(un  == 'british' and pw == 'columbia'):
            return ([{typeCd : 1},])


        print("got "  + un)
        return []

api.add_resource(HelloWorld, '/rso/rs/validatenames')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
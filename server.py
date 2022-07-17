from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import test_func as c

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
# api = Api(app)


print(c.chatbot('Hi'))


@app.route('/', methods=["POST"])
@cross_origin(supports_credentials=True)
def chat():
    message = request.get_json(force=True)['message']
    chatbotRes = c.chatbot(message)
    return {"message": chatbotRes}


# class Data(Resource):
#     @cross_origin(supports_credentials=True)
#     def post(self):
#         message = request.get_json()['message']
#         chatbotRes = c.chatbot(message)
#         return chatbotRes


# class Vars(Resource):
#     def get(self, strVar):
#         print(strVar)
#         print(request.method)
#         return 'Vars!'


# api.add_resource(Data, '/')
# api.add_resource(Vars, '/sup/<string:strVar>')

if __name__ == "__main__":
    app.run(debug=True)  # debug=True because dev mode

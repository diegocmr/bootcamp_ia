from flask import Flask,request,jsonify,make_response
from flask_cors import CORS
from model.Login import Login
from flask.json import JSONEncoder
from datetime import date
import sys

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app,supports_credentials =True, origins= "http://127.0.0.1:8081")


@app.errorhandler(Exception)
def handle_exception(e):
    res = make_response(jsonify({   
        "error": True,         
        "message": str(e)           
    }),401)
    return res
    
@app.route('/login', methods=['POST'])
def login():

    json = request.get_json()   
    login = Login()
    status = login.efetuarLogin(json["login"],json["senha"])
    res = make_response(jsonify({"status":status}), 200 if status else 401)  
      
    if(status):        
        res.set_cookie("api_session", value=login.getToken(),samesite="None",domain="127.0.0.1",secure="False")        
    return res
@app.route('/resumo_cliente', methods=['POST'])
def resumo_cliente():
    
    login = Login().efetuarLoginToken(request.cookies.get('api_session'))
    res = make_response(jsonify({"cliente":login.getUserSession()}), 200)
    
    return res    

if __name__ == '__main__':
    app.run(port=8080,debug=True,host='0.0.0.0')
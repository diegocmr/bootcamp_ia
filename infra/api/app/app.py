from flask import Flask,request,jsonify,make_response
from model.Login import Login
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
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
        res.set_cookie("api_session", value=login.getToken())        
    return res
@app.route('/resumo_cliente', methods=['GET'])
def resumo_cliente():
    
    global userSession
    Login().efetuarLoginToken(request.cookies.get('api_session'))
    res = make_response(jsonify({"cliente":userSession}), 200)
    return res
    

if __name__ == '__main__':
    app.run(port=8080,debug=True,host='0.0.0.0')
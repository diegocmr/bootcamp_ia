from flask import Flask,request,jsonify,make_response
from flask_cors import CORS
from model.Login import Login
from model.Cliente import Cliente
from model.Credito import Credito
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
    }),(401 if str(e) == "O token informado está inválido" else 404))

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

@app.route('/emprestimos', methods=['POST'])
def emprestimos():
    
    login = Login().efetuarLoginToken(request.cookies.get('api_session'))
    cliente = Cliente(login)
    
    res = make_response(jsonify({"data":cliente.getEmprestimos()}), 200)
    
    return res    

@app.route('/cadastro_cliente', methods=['POST'])
def cadastro_cliente():
      
    cliente = Cliente(None)
    json = request.get_json() 
    res = make_response(jsonify({"status":cliente.cadastroCliente(json)}), 200)
    login = Login()
    login.efetuarLogin(json["cnpj"],json["senha"])
    res.set_cookie("api_session", value=login.getToken(),samesite="None",domain="127.0.0.1",secure="False")  
    return res    

@app.route('/cadastro_credito', methods=['POST'])
def cadastro_credito():
    
    login = Login().efetuarLoginToken(request.cookies.get('api_session'))
    credito = Credito(login)
    json = request.get_json() 
    res = make_response(jsonify({"status":credito.cadastroSolicitacao(json)}), 200)   
    return res    
@app.route('/get_credito_analise', methods=['POST'])
def get_credito_analise():
    
    login = Login().efetuarLoginToken(request.cookies.get('api_session'))
    credito = Credito(login)    
    res = make_response(jsonify({"credito":credito.getSolicitacaoAnalise()}), 200)   
    return res    
    

if __name__ == '__main__':
    app.run(port=8080,debug=True,host='0.0.0.0')
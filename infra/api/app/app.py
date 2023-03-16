from flask import Flask,request,jsonify,make_response


from model.Login import Login

from mysql.connector import Error
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    print(json)
    login = Login()
    status = login.efetuarLogin(json["login"],json["senha"])
    res = make_response(jsonify({"status":status}), 200 if status else 401)
    if(status):        
        res.set_cookie("api_session", value=login.getToken())        
    return res


if __name__ == '__main__':
    app.run(port=8080,debug=True,host='0.0.0.0')
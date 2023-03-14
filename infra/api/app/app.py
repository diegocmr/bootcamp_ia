from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return '<p> Hello world </p>'

if __name__ == '__main__':
    app.run(port=8888,debug=True,host='0.0.0.0')
from flask import Flask
from flask import render_template
from flask import request
import flask
import requests
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

f = open('microservicesTable', 'rb')
table = pickle.load(f)
f.close()

@app.route('/API/<path:subpath>') # como guardar requests??
def hello_world(subpath=None):
    print(subpath)
    paths = subpath.split("/")
    route = table[paths[0]]
    day = request.args.get("day") # NÃO MUITO CORRETO. Se houver inputs de outro tipo??
    if day != None:
        URI = route + 'API/' + subpath +'?day=' + day
    else:
        URI = route + 'API/' + subpath 
    r = requests.get(URI)
    data = r.json()
    print(URI)
    return(flask.jsonify(data))

@app.route("/", methods=['GET'])
def test():
    return {"ola":'ola'}
if __name__ == '__main__':
    app.run(port=5004)
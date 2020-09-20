from flask import Flask
from flask import render_template
from flask import request
import flask
import requests
import secretariatsDB

app = Flask(__name__)
db = secretariatsDB.secretariatsDB("mylib")

@app.route('/API/secretariats',  methods = ['GET'])
@app.route('/API/secretariats/<identificador>', methods = ["GET"])
def books(identificador = None):
    b_id = identificador
    if b_id == None:
        lst = db.listSecretariats()
        L = [{'location' : secretariat.location, 'name': secretariat.name, 'description' : secretariat.description, 'openHours' : secretariat.openHours, 'id': secretariat.id} for secretariat in lst]
    else:
        try:
            secretariat = db.showSecretariat(int(b_id))
            L = {'location' : secretariat.location, 'name': secretariat.name, 'description' : secretariat.description, 'openHours' : secretariat.openHours, 'id': secretariat.id}
        except:
            L = {}
    return flask.jsonify(L)

@app.route('/API/secretariats/addsecretariats', methods = ["POST"])
def add_Books_POST():
    data = request.get_json()
    try:
        location = data["location"]
        name = data["name"]
        description = data["description"]
        openHours = data["openHours"]
        s_id = db.addSecretariats(location, name, description, openHours)
        lst = db.showSecretariat(int(s_id))
        L = {'id' : lst.id, 'location': lst.location, 'name' : lst.name, 'description' : lst.description, 'openHours': lst.openHours}
    except:
        L = {}
    return flask.jsonify(L)

@app.route('/API/secretariats/put', methods = ["PUT"])
def change_book():
    data = request.get_json()
    try:
        s_id = data["id"]
        location = data["location"]
        name = data["name"]
        description = data["description"]
        openHours = data["openHours"]
        db.chageSecretariats(location, name, description, openHours, s_id)
        lst = db.showSecretariat(int(b_id))
        L = {'id' : lst.id, 'location': lst.location, 'name' : lst.name, 'description' : lst.description, 'openHours': lst.openHours}
        print(L)
    except:
        L = {}
    return flask.jsonify(L)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.jsonify({"message":"Resource not found"}), 404


if __name__ == '__main__':
    app.run(port=5002)
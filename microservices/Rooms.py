from flask import Flask
from flask import render_template
from flask import request
import flask
import requests
from datetime import date

app = Flask(__name__)

@app.route('/API/rooms/<identificador>', methods = ['GET'])
def rooms(identificador = None):
    r_id = identificador
    try:
        day = request.args.get("day")
        URI = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+r_id + '?day='+day
    except:
        today = date.today()
        day = today.strftime('%d/%m/%Y')
        URI = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+r_id
    r = requests.get(URI)
    data = r.json()
    try:
        name = data["name"]
        events = data["events"]
        campi = data["topLevelSpace"]["name"]
        parent = data["parentSpace"]["type"]
        while parent != "BUILDING":
            parent_id = data["parentSpace"]["id"]
            URI = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'+parent_id
            r = requests.get(URI)
            data = r.json()
            parent = data["parentSpace"]["type"]
            json = flask.jsonify({"name":name, "events": events, "campi": campi, "building": data["parentSpace"]["name"] })
    except:
        json = flask.jsonify(data)
    return json

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.jsonify({"message":"Resource not found"}), 404


if __name__ == '__main__':
    app.run(port=5001)

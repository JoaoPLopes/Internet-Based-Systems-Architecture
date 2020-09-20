from flask import Flask
from flask import render_template
from flask import request
import flask
import requests
import collections, functools, operator 

app = Flask(__name__)

@app.route('/canteen/query')
def query_meal():
    day = request.args.get("day")
    URI = "http://127.0.0.1:5004/API/canteen/meals?day=" + day[8:10]+"/"+day[5:7]+"/"+day[0:4]
    r = requests.get(URI)
    data = r.json()
    almoco = []
    jantar = []
    try:
        for el in data:
            if el["type"] == "Almoço":
                almoco = el["info"]
            if el["type"] == "Jantar":
                jantar = el["info"]
        return render_template("meal.html", al = almoco, jan = jantar, dia = day)
    except:
        return render_template("notAvailable.html",  dia = day)


@app.route('/rooms/query')
def query_rooms():
    r_id = request.args.get("ID")
    URI = "http://127.0.0.1:5004/API/rooms/" + r_id
    r = requests.get(URI)
    data = r.json()
    cla = []
    gen = []
    try:
        for el in data["events"]:
            if el["type"] == "LESSON":
                cla.append(el)
            if el["type"] == "GENERIC":
                gen.append(el)
        return render_template("rooms.html", name = data['name'], build = data['building'], campi = data["campi"], classes = cla, generics = gen)
    except:
        return render_template("invalidID.html")


@app.route('/secretariats/query')
def query_secretariats():
    r_id = request.args.get("ID")
    URI = "http://127.0.0.1:5004/API/secretariats/" + r_id
    r = requests.get(URI)
    data = r.json()
    print(data)
    if data != {}:
        return render_template("secretariats.html", info=data)
    else:
        return render_template("invalidsecretariats.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.jsonify({"message":"Resource not found"}), 404

if __name__ == '__main__':
    app.run(port=5003)
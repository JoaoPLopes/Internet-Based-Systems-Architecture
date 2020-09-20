from flask import Flask
from flask import render_template
from flask import request
import flask
import requests
import canteenDB
from datetime import date

app = Flask(__name__)
db = canteenDB.canteenDB("canteen")

@app.route('/API/canteen/meals/',  methods = ['GET'])
def canteen_week():
    # Show the meals for the whole week of a specific day
    try:
        day = request.args.get("day")
        if day != None: # Se for introduzida data no url
            if day[3] == '0': # if month 0x eliminates 0 from string
                day = day[:3] + day[4:]
            if day[0] == '0': # if day 0x eliminates 
                day = day[1:]
            data = db.showDia(day)
            if data=={}: # Se nao estiver na cache
                URI = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen/?day='+day
                r = requests.get(URI)
                data = r.json()
                db.addSemana(data)
                meal = []
                for d in data:
                    if d["day"] == day:
                        meal = d["meal"]
                data = meal
        else: # Se nao for introduzida data no url
            today = date.today()
            day = today.strftime('%d/%m/%Y') # Dia de hoje
            if day[3] == '0': # if month 0x eliminates 0
                day = day[:3] + oldstr[4:]
            if day[0] == '0': # if day 0x
                day = day[1:]    
            data = db.showDia(day)
            if data=={}: # Se nao estiver na cache
                URI = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen/?day='+day
                r = requests.get(URI)
                data = r.json()
                db.addSemana(data)
                meal = []
                for d in data:
                    if d["day"] == day:
                        meal = d["meal"]
                data = meal
    except:
        data = {"message":"Resource not found"}
    return flask.jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.jsonify({"message":"Resource not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)

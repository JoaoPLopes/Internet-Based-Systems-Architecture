from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import flask
import collections, functools, operator 
import fenixedu
import configparser
import requests
from uuid import uuid4


app = Flask(__name__)
app = Flask(__name__, template_folder='applicationTemplates')

loginName = False
userToken = False
code = False

@app.route('/')
def hello_world():
    return render_template('homePage.html')

@app.route('/validation')
def validation():
    #print(loginName)
    if loginName == False:
        config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
        client = fenixedu.FenixEduClient(config)
        url = client.get_authentication_url()
        return redirect(url)
    else:
        #print(userToken)
        #print(loginName)
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        if (resp.status_code == 200):
            r_info = resp.json()
            #print( r_info)
            image = r_info["photo"]["data"]
            
            validation_code = str(uuid4())

            return render_template("validation.html", name = r_info['name'], imagesrc = image, code = validation_code)
        else:
            return "oops"



@app.route('/mainPage')
def mainPage():
    #print(loginName)
    if loginName == False:
        config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
        client = fenixedu.FenixEduClient(config)
        url = client.get_authentication_url()
        return redirect(url)
    else:
        #print(userToken)
        #print(loginName)
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        if (resp.status_code == 200):
            r_info = resp.json()
            #print( r_info)
            image = r_info["photo"]["data"]
            return render_template("mainPage.html", username = loginName, name = r_info['name'], imagesrc = image)
        else:
            return "oops"


@app.route('/qr_code')
def canteen():
    if loginName == False:
        config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
        client = fenixedu.FenixEduClient(config)
        url = client.get_authentication_url()
        return redirect(url)
    else:
        #print(userToken)
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            return render_template("qr_code.html")
        else:
            return "oops"

@app.route('/auth')
def auth():
    code = request.args['code']
    #print(code)
    # READ CONFIG FILE fenixedu.ini
    config = configparser.ConfigParser()
    config.read('fenixedu.ini')

    # we now retrieve a fenix access token
    payload = {'client_id': config['fenixedu']['client_id'], 'client_secret': config['fenixedu']['client_secret'], 'redirect_uri' : config['fenixedu']['redirect_uri'], 'code' : code, 'grant_type': 'authorization_code'}
    
    response = requests.post('https://fenix.tecnico.ulisboa.pt/oauth/access_token', params = payload)
    
    #print (response.url)
    #print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        #print ('getting user info')
        r_token = response.json()
        #print(r_token)

        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        #print( r_info)

        # we store it
        global loginName
        loginName = r_info['username']
        global userToken
        userToken = r_token['access_token']

        #now the user has done the login
        #return flask.jsonify(r_info)
        #we show the returned infomration
        #but we could redirect the user to the private page
        return redirect('/mainPage') #comment the return jsonify....
    else:
        return 'oops'

@app.route('/logout')
def logout():
    global loginName
    loginName = False
    global userToken
    userToken = False
    global code 
    code = False
    return redirect('https://id.tecnico.ulisboa.pt/cas/logout')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.jsonify({"message":"Resource not found"}), 404


if __name__ == '__main__':
    app.run(port=5100)
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from functools import partial
from datetime import datetime

from service import PibbleDatabase
from service import PibbleBrain
from service import PibbleMotor

from utilities.configLoader import getConfig
from utilities.astroMath import utcFromTimeZone


print = partial(print, flush=True)


INFOS_PATH = os.getcwd() + "/informations.txt"
CONF_PATH = os.getcwd() + "/config.txt"

app = Flask(__name__)
CORS(app)

brain = PibbleBrain.PibbleBrain()
motor = PibbleMotor.PibbleMotor()

config = getConfig(CONF_PATH)
database = PibbleDatabase.PibbleDatabase(brain, config)

software_informations = getConfig(INFOS_PATH)

HOMME_MESSAGE = """<div align='center'>
<h1>Welcome to the PibbleFirmware RESTfull app!</h1>
<br>
Visit the project page on <a href="https://github.com/marklinmax/PibbleFirmware", target="_blank">github</a>!
<p>
Version : {}
<br>
Contributors : {}
</div>""".format(software_informations["version"], ", ".join(software_informations["contributors"]))


print("\nYou are running PibbleFirmware version {}\nMade by : {}\n".format(software_informations["version"], ", ".join(software_informations["contributors"])))

@app.route('/setup/init', methods=['GET'])
def setupInit():
    return jsonify(database.getAlignInit())

@app.route('/setup/reset', methods=['GET'])
def setupReset():
    return jsonify(None)

@app.route('/setup/validate', methods=['GET'])
def setupValidate():
    return jsonify(None)

@app.route('/setup/point', methods=['GET'])
def setupPoint():
    return jsonify(None)


@app.route('/connection', methods=['GET'])
def connexion():
    try:
        args = {}
        for key in request.args.keys():
            args.update({key : request.args.get(key)})
        brain.telescope_coords["latitude"] = float(args["latitude"])
        brain.telescope_coords["longitude"] = float(args["longitude"])
        brain.times["telescope_start_time"] = utcFromTimeZone(datetime.fromtimestamp(float(args["timestamp"])/1000.0), int(args["offset"]))
        brain.times["system_start_time"] = datetime.utcnow()
        brain.times["delta_time"] = brain.times["telescope_start_time"] - brain.times["system_start_time"]
        brain.init()
        database.init()
        return jsonify({"inited" : brain.inited and database.inited})
    except(Exception) as err:
        print("An error occured :\n" + str(err))
        return jsonify({"inited" : False, "error" : str(err)})
    

@app.route('/catalog/<string:table>', methods=['GET'])
def getAllFromTable(table):
    args = {}
    for key in request.args.keys():
        args.update({key : request.args.get(key)})
    return jsonify(database.getAllFromTable(table, args))

@app.route('/catalog/<string:table>/<string:name>', methods=['GET'])
def getObjectByName(table, name=None):
    if name == None:
        name = "NULL"
    return jsonify(database.getObjectByName(table, name))

@app.route('/catalog', methods=['POST'])
def addUserObject():
    
    return jsonify(None)


@app.route('/objects/types', methods=['GET'])
def getTypes():
    return jsonify(database.getTypes())

@app.route('/<string:table>/constellations', methods=['GET'])
def getConstellations(table):
    return jsonify(database.getConstellations(table))


@app.route('/command/track', methods=['GET'])
def getTrack():
    print("track")
    return jsonify(None)

@app.route('/command/move', methods=['GET'])
def move():
    args = {}
    for key in request.args.keys():
        args.update({key : request.args.get(key)})
    return jsonify(motor.commandMove(args)) ## keys are : 'direction' and 'speed'

@app.route('/command/stop', methods=['GET'])
def stop():
    return jsonify(motor.commandStop())


@app.route('/position', methods=['GET'])
def getPositions():
    return jsonify(brain.returnPositions()) ## return ra dec alt az in a dict


@app.route('/informations', methods=['GET'])
def getInfos():
    return jsonify(software_informations)

@app.route('/', methods=['GET'])
def homme():
    return HOMME_MESSAGE

if __name__ == '__main__':
    app.run(debug=True)

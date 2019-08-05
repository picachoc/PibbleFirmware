import os
from flask import Flask, jsonify
from flask_cors import CORS
from service import PibbleDatabase
from utilities/configLoader import *


CONF_PATH = os.getcwd() + "/config.txt"

app = Flask(__name__)
CORS(app)

config = getConfig(CONF_PATH)
database = PibbleDatabase.PibbleDatabase(config)

objs = [{
    "OBJECT": "NGC 7831",
    "OTHER": "IC 1530",
    "TYPE": "GALXY",
    "CON": "AND",
    "RA": "00 07.3",
    "DEC": "+32 37",
    "MAG": "12,8",
    "SUBR": "12,3",
    "U2K": 89,
    "TI": 4,
    "SIZE_MAX": "1.5 m",
    "SIZE_MIN": "0.3 m",
    "PA": 38,
    "CLASS": "Sb",
    "NSTS": "",
    "BRSTR": "",
    "BCHM": "",
    "NGC DESCR": "eF;vS;mE;vF*v nr",
    "NOTES": ""
  },
  {
    "OBJECT": "NGC    5",
    "OTHER": "UGC    62",
    "TYPE": "GALXY",
    "CON": "AND",
    "RA": "00 07.8",
    "DEC": "+35 22",
    "MAG": "13,3",
    "SUBR": "13,2",
    "U2K": 89,
    "TI": 4,
    "SIZE_MAX": "1.2 m",
    "SIZE_MIN": "0.7 m",
    "PA": 115,
    "CLASS": "Elliptical",
    "NSTS": "",
    "BRSTR": "",
    "BCHM": "",
    "NGC DESCR": "vF;vS;N=*13;14",
    "NOTES": "compact"
  }]

@app.route('/catalog/<string:table>', methods=['GET'])
def getAllFromTable(table):
    return jsonify(database.getAllFromTable(table))

@app.route('/catalog/<string:table>/<string:name>', methods=['GET'])
def getObjectByName(table, name=None):
    if name == None:
        name = "NULL"
    return jsonify(database.getObjectByName(table, name))

@app.route('/objects/types', methods=['GET'])
def getTypes():
    return jsonify(database.getTypes())

@app.route('/<string:table>/constellations', methods=['GET'])
def getConstellations(table):
    return jsonify(database.getConstellations(table))

@app.route('/command/track', methods=['GET'])
def get_track():
    print("track")
    return jsonify(objs[0]["OTHER"])



if __name__ == '__main__':
    app.run(debug=True)

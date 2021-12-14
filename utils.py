from flask import jsonify
import os, json
#Denies user from access
def deny():
    return jsonify({"Error": "Forbidden"}),403

def getTMPCurrentWeather():
    tmp_list = []
    with open(os.path.join('WeatherApps','tmp','currentWeather.json'),'r') as f:
        tmp = json.loads(f.read())
        
        tmp_list.append(tmp)

    return tmp_list

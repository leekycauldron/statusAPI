import json, sys, threading
from os import stat
from flask import Flask, jsonify, request
from requests.api import get
from Threads.currentWeatherThread import currentWeatherThread
sys.path.insert(0,"./middleware")
sys.path.insert(1,"./TodoistApps")
sys.path.insert(2,"./Threads")
from auth import Authenticate
from getTasks import getTasks
from currentWeatherThread import currentWeatherThread
from utils import deny, getTMPCurrentWeather
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
debug = True
PORT = 80

# @route: /
# @access: Public
# @description: This route should not return useful info, for test purposes only
@app.route('/')
def index():
    status = 200
    message = jsonify({'message':'Hello, World!'})
 
    return message,status


# @route: /todoist/tasks
# @access: Private
# @description: This route returns all the todoist tasks in project "Tasks". Limit to 2 total request per 2 seconds.
# TODO: Rate limit to 1 request per 2 seconds.
@app.route("/todoist/tasks")
def todoistTasks():
    if not Authenticate("567g8uibvcrVA76L7g8bE7cv8b9Rbv7I5f23h234ojEkj0j09j76866hm9"):
        return deny()
    tasks = getTasks()
    return jsonify(tasks)

# @route: /weather/now
# @access: Private
# @description: This route returns the current weather data. API request sent every 30 minutes will be saved in a file
# Every user will access the user to prevent being API rate limited.

@app.route("/weather/now")
def weatherNow():
    if not Authenticate("567g8uibvcrVA76L7g8bE7cv8b9Rbv7I5f23h234ojEkj0j09j76866hm9"):
        return deny()
    return jsonify(getTMPCurrentWeather())
 


if __name__ == "__main__":
    #Get weather every 30 minutes
    thread1 = threading.Thread(target=currentWeatherThread)
    thread1.daemon = True
    thread1.start()
    if debug:
        app.run(port=PORT)
    else:
        app.run(host="0.0.0.0",port=PORT)
import json, sys, threading, argparse
from os import stat
from flask import Flask, jsonify, request
from requests.api import get
from Threads.currentWeatherThread import currentWeatherThread
sys.path.insert(0,"./middleware")
sys.path.insert(1,"./TodoistApps")
sys.path.insert(2,"./Threads")
sys.path.insert(3,"./UberEatsApps")
from auth import Authenticate
from getTasks import getTasks
from finishTask import finishTask
from currentWeatherThread import currentWeatherThread
from fetchLinks import fetchLinks
from notificationListenerThread import notificationListenerThread
from utils import deny, getTMPCurrentWeather
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

PORT = 80

# A variable used to tell the Uber Eats thread if they need to check the links.
# False by default.

uberEats = False


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

# @route: /todoist/closeTask
# @access: Private
# @description: This route deletes todoist task given its ID.
@app.route("/todoist/closeTask", methods=["DELETE"])
def closeTask():
    if not Authenticate("567g8uibvcrVA76L7g8bE7cv8b9Rbv7I5f23h234ojEkj0j09j76866hm9"):
        return deny()
    taskToFinish = json.loads(request.data)
    
    successDelete = finishTask(taskToFinish["id"])
    if not successDelete:
        return jsonify({"error":"There was an error removing the task, please try again."}), 500
    return jsonify({"message":"Task successfully removed."})
  
    


# @route: /weather/now
# @access: Private
# @description: This route returns the current weather data. API request sent every 30 minutes will be saved in a file
# Every user will access the user to prevent being API rate limited.

@app.route("/weather/now")
def weatherNow():
    if not Authenticate("567g8uibvcrVA76L7g8bE7cv8b9Rbv7I5f23h234ojEkj0j09j76866hm9"):
        return deny()
    return jsonify(getTMPCurrentWeather())


# @route: /ubereats
# @access: Private
# @description: This route fetches all current uber eats deliveries and provides the user with the link. 

@app.route("/ubereats")
def uberEats():
    global uberEats
    if not Authenticate("567g8uibvcrVA76L7g8bE7cv8b9Rbv7I5f23h234ojEkj0j09j76866hm9"):
        return deny()

    #Get links
    links = fetchLinks()
    print(links)
    if not links:
        return jsonify({"message":"There are no links at this time."})
    #get thread to run
    uberEats = True

    #return link

    return jsonify({"Links: ": links})








if __name__ == "__main__":
    #Get weather every 30 minutes
    thread1 = threading.Thread(target=currentWeatherThread)
    thread1.daemon = True
    thread1.start()
    #Listens for phone notifications and does stuff with it.
    thread2 = threading.Thread(target=notificationListenerThread)
    thread2.daemon = True
    thread2.start()
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", type=str, required=True,
        help="mode to run server (localhost/network). Options (0 or 1) respectively.")

    args = vars(ap.parse_args())
    mode = args["mode"]

    if mode == "0":
        app.run(port=PORT)
    elif mode == "1":
        app.run(host="0.0.0.0",port=PORT)
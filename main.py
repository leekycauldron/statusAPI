import json, sys
from os import stat
from flask import Flask, jsonify, request
from requests.api import get
sys.path.insert(0,"./middleware")
sys.path.insert(1,"./TodoistApps")
from auth import Authenticate
from getTasks import getTasks
app = Flask(__name__)

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
    tasks = getTasks()
    return jsonify(tasks)

if __name__ == "__main__":
    if debug:
        app.run(port=PORT)
    else:
        app.run(host="0.0.0.0",port=PORT)
import json, sys
from os import stat
from flask import Flask, jsonify, request
sys.path.insert(0,"./middleware")
from auth import Authenticate
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


# @route: /
# @access: Private
# @description: This route returns weather data to the authenticated user. The (1) user will be rate limited to 2 requests per hour.
@app.route("/weather")
def weather():
    

if __name__ == "__main__":
    if debug:
        app.run(port=PORT)
    else:
        app.run(host="0.0.0.0",port=PORT)
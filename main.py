import json
from flask import Flask, jsonify
app = Flask(__name__)


# This route should not return useful info
@app.route('/',methods=["GET"])
def index():
    return "Hello World!"

app.run(host="0.0.0.0",port=80)
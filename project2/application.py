import os

from flask import Flask, render_template, request, redirect, session, jsonify
from flask_socketio import SocketIO, emit

from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Turn off alphabetical sorting for JSON responses
# https://flask.palletsprojects.com/en/1.1.x/config/#config
app.config["JSON_SORT_KEYS"] = False

channels = []
messages = []


@app.route("/")
def index():

    return render_template("index.html", channels=channels)


@app.route("/create_channel", methods=['POST'])
def create_channel():
    """Ajax endpoint for channel creation"""

    # Get data from request
    name = request.form.get('name').rstrip().replace(' ', '-')
    if not name:
        return jsonify({"success": False, "error": "No channel name detected"})

    # Update channels list in memory
    if name in channels:
        return jsonify({"success": False, "error": "This channel name is already in use"})
    else:
        channels.append(name)

    # Prepare and send response
    return jsonify({"success": True, "channels": channels})


@socketio.on("send message")
def send(data):
    """Websocket method to send a message"""

    return None

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

# Mock data for milestone 2
c1 = Channel('default')
channels.append(c1)
m1 = Message(c1, 'Nikita Soshenko', 'Hi, guys!')
m2 = Message(c1, 'Tony Stark', 'We are avengers!!!')
m3 = Message(c1, 'Illidan Stormrage', 'Demons? Demons')
m4 = Message(Channel('123'), 'Another user', 'Another channel')
messages.append(m1)
messages.append(m2)
messages.append(m3)
messages.append(m4)


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
    for channel in channels:
        if channel.name == name:
            return jsonify({"success": False, "error": "This channel name is already in use"})
    channel = Channel(name)
    channels.append(channel)

    # Prepare and send response
    return jsonify({"success": True, "channel": channels[-1].name})


@app.route("/get_messages", methods=['POST'])
def get_messages():
    """Ajax endpoint for getting all messages from channel"""

    # Get data from request
    channel = request.form.get('channel').strip('#')
    print(channel)
    if not channel:
        return jsonify({"success": False, "error": "No channel in request"})

    # Search for messages in the channel
    response = []
    for message in messages:
        if message.channel.name == channel:
            response.append({"author": message.user, "time": str(message.time), "contents": message.text})

    # Send response
    if not response:
        return jsonify({"success": False, "error": "No messages in this channel"})
    else:
        return jsonify({"success": True, "messages": response})


@socketio.on("send message")
def send_message(data):
    """Websocket method to send a message"""

    # Find a channel object with the passed name
    for channel in channels:
        if channel.name == data['channel'].strip('#'):
            current = channel
            break

    # Store new message
    message = Message(current, data['user'], data['message'])
    messages.append(message)
    print(message.channel.name, message.user, message.text)

    # Announce new message to websockets
    emit('announce message', {"message": {"channel": message.channel.name, "author": message.user,
                                "time": str(message.time), "contents": message.text}}, broadcast=True)


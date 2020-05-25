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

"""
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
"""

# Mock data for 100 messages per channel restriction
c1 = Channel('default')
channels.append(c1)
for i in range(99):
    messages.append(Message(c1, 'Nikita Soshenko', f'{i+1}'))

@app.route("/")
def index():

    return render_template("index.html", channels=channels)


@socketio.on("create channel")
def create_channel(data):
    """Web socket support for channel creation"""

    # Get channel name
    name = data['channel'].strip('#')

    # Update channels list in memory
    for channel in channels:
        if channel.name == name:
            return
    channel = Channel(name)
    channels.append(channel)

    # Send response
    emit('announce channel', {"channel": channels[-1].name}, broadcast=True)


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



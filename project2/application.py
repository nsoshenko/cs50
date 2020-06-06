# -*- coding: utf-8 -*-

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

messages = {}
channels = []

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
messages[c1.name] = []
for i in range(150):
    messages[c1.name].append(Message(c1, 'Nikita Soshenko', f'{i+1}'))
messages['default'].append(Message(c1, 'medusa', '123'))  # mock for delete


@app.route("/")
def index():

    return render_template("index.html", channels=channels)


@socketio.on("create channel")
def create_channel(data):
    """Web socket support for channel creation"""

    # Get channel name
    name = data['channel'].strip('#').replace(' ', '-')[:24]

    # Check if there is same channel in memory
    for channel in channels:
        if channel.name == name:
            emit('announce channel', {'success': False, 'channel': name,
                                      'error': 'This channel already exists'}, broadcast=True)
            return

    # Update channel list in memory
    channel = Channel(name)
    channels.append(channel)
    messages[channel.name] = []

    # Send response
    emit('announce channel', {'success': True, 'channel': channels[-1].name}, broadcast=True)


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
    for message in messages[channel]:
        response.append({"id": message.id, "author": message.user,
                         "date": message.time.strftime('%d.%m.%y'),
                         "time": message.time.strftime('%H:%M:%S'),
                         "contents": message.text})

    # Send response
    if not response:
        return jsonify({"success": False, "error": "No messages in this channel yet"})
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

    # Check for empty current if no channel found
    # TBD

    # Store new message
    message = Message(current, data['user'], data['message'])
    messages[current.name].append(message)

    # Make sure to store only 100 messages per channel
    for x in range(len(messages[current.name]) - 100):
        del messages[current.name][0]

    # Announce new message to websockets
    emit('announce message', {"message": {"id": message.id, "channel": message.channel.name, "author": message.user,
                              "date": message.time.strftime('%d.%m.%y'), "time": message.time.strftime('%H:%M:%S'),
                              "contents": message.text}}, broadcast=True)


@socketio.on("delete message")
def delete_message(data):
    """Websocket method for deleting messages"""

    # Find a channel object with the passed name
    for channel in channels:
        if channel.name == data['channel']:
            current = channel
            print(current.name)
            print(messages[current.name][-1].text)
            break

    # Find and delete the message in channel
    for message in messages[current.name]:

        if message.id == int(data['id']):

            if message.user == data['user']:
                print(message.text)
                del message
                emit('delete message', {'success': True, 'id': data['id']}, broadcast=True)
            else:
                print("ERROR")
                emit('delete message', {'success': False,
                                        'error': "Trying to delete message of another user"}, broadcast=True)
            break


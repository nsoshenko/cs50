from datetime import datetime


class Message:

    counter = 1

    def __init__(self, channel, user, text):
        self.id = Message.counter
        self.channel = channel
        self.user = user
        self.text = text
        self.time = datetime.now()  # today() ?

        Message.counter += 1


class Channel:

    def __init__(self, name):
        self.name = name

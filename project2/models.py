from datetime import datetime


class Message:

    def __init__(self, channel, user, text):
        self.channel = channel
        self.user = user
        self.text = text
        self.time = datetime.now()  # today() ?


class Channel:

    def __init__(self, name):
        self.name = name

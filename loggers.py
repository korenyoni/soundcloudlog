import soundcloud
import time

from colors import bcolors
from event import Event
from eventList import EventList


class AbstractLog():
    client = None
    eventList = EventList()

    def log(self):
        if not self.eventList.sorted:
            self.eventList.sortList()
        for event in self.eventList:
            if not event.logged:
                print(event.pretty_timestamp() + " " + event.content)
                event.logged = True


class CommentsLog(AbstractLog):
    """
    logs comments belonging to user
    """
    username = None
    tracks = None

    def __init__(self, client, username=None):
        if not isinstance(client, soundcloud.Client):
            raise TypeError("client must be soundcloud.Client")
        self.client = client
        self.username = username

    def populate(self):
        if self.username is None:
            user_id = self.client.get('/me').id
            self.tracks = self.client.get('/users/' + str(user_id) + '/tracks')
        self.tracks = self.client.get('/users/' + self.username + '/tracks')
        for track in self.tracks:
            track_comments = self.client.get('/tracks/' + str(track.id) + '/comments')
            for comment in track_comments:
                eventContent = bcolors.OKBLUE + comment.user['username'] \
                               + bcolors.ENDC + bcolors.WARNING + '(' + track.title \
                               + ')' + bcolors.ENDC + ': ' + bcolors.FAIL + comment.body
                event = Event(comment.created_at, eventContent)
                self.eventList.append(event)

    def loop(self):
        time.sleep(5)
        self.populate()
        self.log()
        self.loop()

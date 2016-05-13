import soundcloud, time, sys, codecs

from colors import bcolors
from event import Event
from eventlist import EventList

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

class AbstractLog():
    client = None
    event_list = EventList()
    print_delay = False

    def log(self):
        if not self.event_list.sorted: #first time
            self.event_list.sortList()
            self.event_list.sorted = True
        for event in self.event_list:
            if not event.logged:
                if self.print_delay : self.delay_print()
                sys.stdout.buffer.write(bytes(event.pretty_timestamp() + ' ' + event.content + '\n', encoding='utf-8'))
                sys.stdout.flush()
                event.logged = True

    def delay_print(self):
        time.sleep(0.12) # delay printing to stdout

class CommentsLog(AbstractLog):
    """
    logs comments belonging to user
    """
    username = None
    tracks = None

    def __init__(self, client, username=None, delay=False):
        if not isinstance(client, soundcloud.Client):
            raise TypeError("client must be soundcloud.Client")
        self.client = client
        self.username = username
        self.print_delay = delay

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
                self.event_list.append(event)

    def loop(self):
        time.sleep(5)
        self.populate()
        self.log()
        self.loop()

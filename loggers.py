import soundcloud, time, sys, codecs

from colors import bcolors
from event import Event
from eventlist import EventList

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

    def sleep(self):
        time.sleep(5)

class EventLog(AbstractLog):
    """
    logs comments belonging to user
    """
    username = None
    tracks = None

    def __init__(self, client, username=None, delay=False, log_comments=False, log_tracks=False):
        if not isinstance(client, soundcloud.Client):
            raise TypeError("client must be soundcloud.Client")
        self.client = client
        self.username = username
        self.print_delay = delay
        self.log_comments = log_comments
        self.log_tracks = log_tracks

    def populate(self):
        if self.username is None:
            user_id = self.client.get('/me').id
            self.tracks = self.client.get('/users/' + str(user_id) + '/tracks')
        self.tracks = self.client.get('/users/' + self.username + '/tracks')
        for track in self.tracks:
            track_comments = self.client.get('/tracks/' + str(track.id) + '/comments')
            if self.log_tracks:
                track_event = Event(track.created_at, bcolors.OKGREEN + self.username + " uploaded "
                                    + bcolors.OKBLUE + track.title + bcolors.ENDC)
                self.event_list.append(track_event)
            for comment in track_comments:
                eventContent = bcolors.OKBLUE + comment.user['username'] \
                               + bcolors.ENDC + bcolors.WARNING + '(' + track.title \
                               + ')' + bcolors.ENDC + ': ' + bcolors.FAIL + comment.body
                if self.log_comments:
                    comment_event = Event(comment.created_at, eventContent)
                    self.event_list.append(comment_event)

    def loop(self):
        try:
            self.sleep()
            self.populate()
            self.log()
            self.loop()
        except KeyboardInterrupt:
            print("\nGoodbye.")

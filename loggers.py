import soundcloud
from colors import bcolors

class AbstractLog():
    client = None

class CommentsLog(AbstractLog):
    """
    logs comments belonging to user
    """
    tracks = None
    def __init__(self, client):
        if not isinstance(client, soundcloud.Client):
            raise TypeError("client must be soundcloud.Client")
        self.client = client

    def log(self, username=None):
        if username is None:
            user_id = self.client.get('/me').id
            self.tracks = self.client.get('/users/' + str(user_id) + '/tracks')
        self.tracks = self.client.get('/users/' + username + '/tracks')
        for track in self.tracks:
            track_comments = self.client.get('/tracks/' + str(track.id) + '/comments')
            for comment in track_comments:
                print(bcolors.OKBLUE + comment.user['username']
                      + bcolors.ENDC + bcolors.WARNING + '(' + track.title
                      + ')' + bcolors.ENDC + ': ' + bcolors.FAIL + comment.body )

import argparse, configparser, os, soundcloud, sys

from loggers import EventLog
from colors import bcolors

config_file_name = '.soundcloudlog.conf'

# Handle arguments
parser = argparse.ArgumentParser(description="Pretty print SoundCloud events up to now")
parser.add_argument("username", help="username of user to log events for")
parser.add_argument('-c', help="log all comments from this user's tracks", action="store_true")
parser.add_argument('-t', help="log all tracks from this user", action="store_true")
parser.add_argument('-d', help="delay printing of each event so that events aren't printed all at once", action='store_true')
args = parser.parse_args()

# Read configuration
config_path = os.path.expanduser('~/') + config_file_name
if os.path.isfile(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    config_auth = config['auth']
    client = soundcloud.Client(
        client_id=config_auth['client_id'],
        client_secret=config_auth['client_secret'],
        redirect_uri=config_auth['redirect_uri'],
        access_token=config_auth['access_token'])

    try:
        if args.username is not None:
            commentsLog = EventLog(client, username=args.username,
                                   delay=args.d, log_comments=args.c, log_tracks=args.t)
            commentsLog.loop()
        else:
            parser.print_help()
    except IOError:
        print("Check your internet connection.")
else:
    print('No config found. Place file in ' + config_file_name)

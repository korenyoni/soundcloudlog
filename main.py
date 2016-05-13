import argparse
import configparser
import os
import soundcloud

from loggers import CommentsLog

config_file_name = '.soundcloudlog.conf'

# Handle arguments
parser = argparse.ArgumentParser(description="Pretty print SoundCloud events up to now")
parser.add_argument('-c', help="log all comments from this user's tracks", metavar='username')
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
        if args.c is not None:
            commentsLog = CommentsLog(client, username=args.c, delay=args.d)
            commentsLog.loop()
        else:
            parser.print_help()
    except IOError:
        print("Check your internet connection.")
else:
    print('No config found. Place file in ' + config_file_name)

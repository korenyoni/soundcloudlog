import soundcloud, configparser, os, argparse
from loggers import CommentsLog

config_file_name = '.soundcloudlog.conf'

#Handle arguments
parser = argparse.ArgumentParser(description="Pretty print SoundCloud events up to now")
parser.add_argument('-c', action='store_true', help="log all comments from your tracks")
args = parser.parse_args()

#Read configuration
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

    commentsLog = CommentsLog(client)

    if args.c:
        commentsLog.log('jromic')
    else:
        parser.print_help()
else:
    print('No config found. Place file in ' + config_file_name)

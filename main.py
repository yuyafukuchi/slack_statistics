import configparser
from collections import defaultdict
import datetime
from logging import basicConfig, getLogger, DEBUG, INFO
from slack import WebClient
# --------------------------------------------------
# loggingの設定
# --------------------------------------------------
logger = getLogger(__name__)
basicConfig(level=INFO)

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')


# --------------------------------------------------
# グローバル変数の定義
# --------------------------------------------------
SLACK_CHANNEL_NAMES = ['general','random']
TOKEN = config_ini['Auth']['TOKEN']
MAX_MESSAGE = 500 #between 1 and 1000
oldest = '2020-04-01'
latest = '2020-05-01'
timeformat = "%Y-%m-%d"
dt_oldest = datetime.datetime.strptime(oldest,timeformat)
dt_latest = datetime.datetime.strptime(latest,timeformat)

message_counts = defaultdict(int)
reaction_counts = defaultdict(int)
client = WebClient(TOKEN)

def convert_userid_to_username(userid):
    info = client.users_info(user=userid)
    if not info['ok']:
        logger.error(info['error'])
        return
    else:
        if info.get('user'):
            user = info['user']
            return user['real_name']
        else:
            raise Exception

def convert_channel_names_to_ids():
    channels_list = client.channels_list()
    ids= {}
    if channels_list['ok']:
        for channel in channels_list['channels']:
            if channel.get('name') and channel['name'] in SLACK_CHANNEL_NAMES:
                ids[channel['id']] = channel['name']
        return ids
    else:
        logger.error(channels_list['error'])

def fetch_history():
    SLACK_CHANNEL_IDS = convert_channel_names_to_ids()
    logger.info(f'fetching messages from {oldest} to {latest}')


    for channel_id,channel_name in SLACK_CHANNEL_IDS.items():
        logger.info(f'fetching messages from {channel_name}')
        json_data = client.channels_history(
            channel=channel_id, 
            count = MAX_MESSAGE,
            latest=str(dt_latest.timestamp()),
            oldest=str(dt_oldest.timestamp())
        )

        if not json_data['ok']:
            logger.error(json_data['error']+"!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue

        messages = json_data['messages']

        for message in messages:
            message_counts[message['user']]+=1

            if not message.get('reactions'): continue

            for r in  message['reactions']:
                for user in r['users']:
                    reaction_counts[user] += 1

if __name__ == '__main__':
    fetch_history()

    for userid,count in message_counts.items():
        print(convert_userid_to_username(userid),count)

    # for userid,count in reaction_counts.items():
    #     print(convert_userid_to_username(userid),count)
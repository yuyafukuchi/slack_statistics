import json
import datetime
import requests
import configparser
from slack import WebClient
from collections import defaultdict
from logging import basicConfig, getLogger, DEBUG, INFO

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
SLACK_CHANNEL_NAMES = config_ini['Config']['TARGET_CHANNELS'].split(',')
TOKEN = config_ini['Auth']['TOKEN']
MAX_MESSAGE = 20 #between 1 and 1000
MAX_RANKING = int(config_ini['Config']['MAX_RANKING'])
TIMEFORMAT = "%Y-%m-%d"

client = WebClient(TOKEN)

def convert_userid_to_username(userid):
    info = client.users_profile_get(user=userid)
    if not info['ok']:
        logger.error(info['error'])
        return
    else:
        user = info['profile']
        return user['real_name']

def convert_channel_names_to_ids():
    channels_list = client.conversations_list(types="public_channel,private_channel")
 
    ids= {}
    if channels_list['ok']:
        for channel in channels_list['channels']:
            if channel['name'] in SLACK_CHANNEL_NAMES:
                ids[channel['id']] = channel['name']
        return ids
    else:
        logger.error(channels_list['error'])

def fetch_historys(dt_latest,dt_oldest):
    SLACK_CHANNEL_IDS = convert_channel_names_to_ids()
    message_counts = defaultdict(int)
    reaction_counts = defaultdict(int)

    logger.info(f'fetching messages from {dt_oldest.strftime(TIMEFORMAT)} to {dt_latest.strftime(TIMEFORMAT)}')

    def fetch_history(dt_latest,dt_oldest,channel_id,cursor=None):
        if cursor:
            json_data = client.conversations_history(
                channel=channel_id, 
                count = MAX_MESSAGE,
                latest=str(dt_latest.timestamp()),
                oldest=str(dt_oldest.timestamp()),
                cursor =cursor
            )
        else:
            json_data = client.conversations_history(
                channel=channel_id, 
                count = MAX_MESSAGE,
                latest=str(dt_latest.timestamp()),
                oldest=str(dt_oldest.timestamp())
            )

        if not json_data['ok']:
            logger.error(json_data['error']+"!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return

        messages = json_data['messages']
        for message in messages:
            message_counts[message['user']]+=1

            if not message.get('reactions'): continue

            for r in  message['reactions']:
                for user in r['users']:
                    reaction_counts[user] += 1   
        if json_data['has_more'] and json_data['response_metadata']['next_cursor']:
            fetch_history(
                dt_latest=dt_latest,
                dt_oldest=dt_oldest,
                channel_id=channel_id,
                cursor=json_data['response_metadata']['next_cursor']
            )

    for channel_id,channel_name in SLACK_CHANNEL_IDS.items():
        logger.info(f'fetching messages from {channel_name}')
        fetch_history(
            dt_latest=dt_latest,
            dt_oldest=dt_oldest,
            channel_id=channel_id
        )        
    
    return message_counts,reaction_counts



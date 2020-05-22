import requests
import configparser
import datetime
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

SLACK_CHANNEL_ID = 'CDWM698CQ'
SLACK_URL = "https://slack.com/api/channels.history"
TOKEN = config_ini['Auth']['TOKEN']
oldest = '2020-04-01'
latest = '2020-05-01'
timeformat = "%Y-%m-%d"
dt_oldest = datetime.datetime.strptime(oldest,timeformat)
dt_latest = datetime.datetime.strptime(latest,timeformat)

def fetch_text():
    logger.info(f'fetching messages from {oldest} to {latest}')

    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN,
        "latest": dt_latest.timestamp(),
        "oldest": dt_oldest.timestamp()
    }

    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    # print(json_data['messages'])
    msgs = json_data['messages']
    # return [msg['text'] for msg in msgs]

if __name__ == '__main__':
    fetch_text()
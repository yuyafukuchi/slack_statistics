import requests
import configparser

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')


SLACK_CHANNEL_ID = 'CDWM698CQ'
SLACK_URL = "https://slack.com/api/channels.history"
TOKEN = config_ini['Auth']['TOKEN']



def fetch_text():
    print(TOKEN)
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN
    }
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    print(json_data['messages'][0])
    msgs = json_data['messages']
    # return [msg['text'] for msg in msgs]

if __name__ == '__main__':
    fetch_text()
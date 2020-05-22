import requests

SLACK_CHANNEL_ID = 'CDWM698CQ'
SLACK_URL = "https://slack.com/api/channels.history"
TOKEN = "9AdmJjQPZxra8wlsBC514mVA"

def fetch_text():
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN
    }
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    print(json_data)
    msgs = json_data['messages']
    return [msg['text'] for msg in msgs]

if __name__ == '__main__':
    fetch_text()
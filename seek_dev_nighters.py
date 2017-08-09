import requests
from datetime import datetime
from pytz import timezone


def load_attempts():
    pages = 2
    for page in range(pages):
        page += 1
        params = {'page': page}
        response = requests.get('https://devman.org/api/challenges/solution_attempts/', params)
        if response.ok:
            attempts = response.json()
            for attempt in attempts['records']:
                yield {
                    'username': attempt['username'],
                    'timestamp': attempt['timestamp'],
                    'timezone': attempt['timezone'],
                }


def get_midnighters(user_data):
    night_ending = 6
    tz = user_data['timezone']
    if user_data['timestamp']:
        server_time = datetime.fromtimestamp(user_data['timestamp'])
        user_time = timezone(tz).fromutc(server_time)
        if user_time.hour < night_ending:
            return True


if __name__ == '__main__':
    for user_data in load_attempts():
        if get_midnighters(user_data):
            print(user_data)

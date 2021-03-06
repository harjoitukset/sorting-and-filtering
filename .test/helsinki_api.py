import json
import urllib.request
from datetime import datetime, timedelta
from functools import lru_cache

EVENTS_API_URL = 'http://open-api.myhelsinki.fi/v1/events/'


@lru_cache
def get_events():
    with urllib.request.urlopen(EVENTS_API_URL) as response:
        json_response = json.load(response)
        return json_response['data']  # 'data' on lista tapahtumista


def get_start_time(event):
    return event['event_dates'].get('starting_day', '')


def get_name(event):
    return (event['name']['fi'] or event['name']['en'] or event['name']['sv'] or event['name']['zh']).strip()


def filter_events_by_days(events, min_days, max_days):
    start = (datetime.utcnow() + timedelta(days=min_days)).isoformat()
    end = (datetime.utcnow() + timedelta(days=max_days)).isoformat()

    return [e for e in events if get_start_time(e) and start <= get_start_time(e) <= end]


def sort_chronologically(events: list):
    return sorted(events, key=get_start_time)

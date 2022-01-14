from pytest import fixture
import urllib.request
import json
from datetime import datetime, timedelta
import os
from functools import lru_cache

EVENTS_API_URL = 'http://open-api.myhelsinki.fi/v1/events/'


@fixture
def student_answer():
    with open(os.path.join(os.path.dirname(__file__), '../student_output.txt')) as f:
        return f.read()


@lru_cache
def get_events():
    with urllib.request.urlopen(EVENTS_API_URL) as response:
        json_response = json.load(response)
        return json_response['data']  # 'data' on lista tapahtumista


def get_start_time(event):
    return event['event_dates'].get('starting_day', '')


def get_name(event):
    return (event['name']['fi'] or event['name']['en'] or '').strip()


def filter_events_by_days(events, min_days, max_days):
    start = (datetime.utcnow() + timedelta(days=min_days)).isoformat()
    end = (datetime.utcnow() + timedelta(days=max_days)).isoformat()

    return [e for e in events if get_start_time(e) and start <= get_start_time(e) <= end]


def sort_chronologically(events: list):
    return sorted(events, key=get_start_time)

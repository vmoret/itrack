"""tools.py

Provides functions to search iTrack issues.
"""
import datetime as dt
from functools import wraps
import urllib
import json

import requests
import pandas as pd

from .decorators import key_error, type_error, value_error, set_index, to_dataframe
from .parsers import parse_issue


def parse_issues(func):
            
    @wraps(func)
    def wrapper(*args, **kwargs):
        yield from (parse_issue(x) for x in func(*args, **kwargs))
    
    return wrapper

API_BASE = 'https://itrack.barco.com:443/rest/api/2'


@set_index('key')
@to_dataframe
@parse_issues
def search(jql, auth):
    
    def search_once(jql, auth, start_at=0, max_results=100):
        qstring = 'jql={}&startAt={:d}&maxResults={:d}'.format(
            urllib.parse.quote_plus(jql), start_at, max_results)
        url = API_BASE + '/search?' + qstring
        response = requests.get(url, auth=auth)
        try:
            data = response.json()
            return data['issues'], data['total']
        except json.JSONDecodeError:
            return [], 0

    retrieved = 0
    total = 1 # needs to be bigger than retrieved...

    while retrieved < total:
        items, total = search_once(jql, auth=auth, start_at=retrieved)
        retrieved += len(items)
        yield from iter(items)
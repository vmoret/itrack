"""parsers.py

Provides functions to parse iTrack issues.
"""
import datetime as dt

from .decorators import key_error, type_error, value_error


def pluck_fields(*keys):
    @key_error
    def plucker(fields, keys=keys):
        first, *rest = keys
        value = fields[first]
        return value if not rest else plucker(value, keys=rest)
    return plucker
    
pluck_issue_type = pluck_fields('fields', 'issuetype', 'name')
pluck_severity = pluck_fields('fields', 'customfield_10002', 'value')
pluck_project = pluck_fields('fields', 'project', 'name')
pluck_status = pluck_fields('fields', 'status', 'name')
pluck_assignee = pluck_fields('fields', 'assignee', 'name')
pluck_summary = pluck_fields('fields', 'summary')
    
def pluck_date(name):
    
    def splitdate(s):
        return s.split('T')[0] if isinstance(s, str) else None

    @type_error
    @value_error
    def strptime(s, fmt=r'%Y-%m-%d'):
        return dt.datetime.strptime(s, fmt)
    
    def wrapper(*args, **kwargs):
        return strptime(splitdate(pluck_fields('fields', name)(*args, **kwargs)))
    
    return wrapper

pluck_created = pluck_date('created')
pluck_resolutiondate = pluck_date('resolutiondate')
pluck_updated = pluck_date('updated')

def get_key(data):
    return data['key']

MAPPING = dict(key=get_key,
               issue_type=pluck_issue_type,
               severity=pluck_severity,
               project=pluck_project,
               status=pluck_status,
               assignee=pluck_assignee,
               summary=pluck_summary,
               created=pluck_created,
               resolutiondate=pluck_resolutiondate,
               updated=pluck_updated)

def parse_issue(data):
    return {k: func(data) for k, func in MAPPING.items()}

from facebook import GraphAPI
import requests
import arrow
import re

from renderer import render

import config

graph = GraphAPI(access_token=config.ACCESS_TOKEN, version="2.5")

def get_latest_events_raw():
    id = config.EVENT_PAGE + "/events"
    return graph.get_object(
        id,
        fields="id,name,start_time,end_time,attending_count,interested_count"
    )['data']


EVENT_PICTURE_RE = re.compile('scaledImageFitHeight(.*?)src="([^"]+)')

def get_full_event_picture(url):
    res = requests.get(url)
    match = EVENT_PICTURE_RE.search(res.text)
    if match is None:
        return None
    else:
        return match.group(2).replace('&amp;', '&')

class Event(object):
    def __init__(self, data):
        self.id = data['id']
        self.url = u"https://www.facebook.com/events/" + self.id
        self.name = data['name']
        self.start_time = arrow.get(data['start_time'])
        if 'end_time' in data:
            self.end_time = arrow.get(data['end_time'])
        self.attending_count = data['attending_count']
        self.interested_count = data['interested_count']

    def fetch_full_picture(self):
        self.picture_url = get_full_event_picture(self.url)

    def is_active(self):
        if hasattr(self, 'end_time'):
            return self.end_time > arrow.now()
        else:
            return self.start_time > arrow.now()

def aws_func(event, context):
    events = [Event(data) for data in get_latest_events_raw()]
    events = filter(lambda e: e.is_active(), events)
    events = events[::-1]

    if len(events) > 0:
        main_event = events.pop(0)
        main_event.fetch_full_picture()
    else:
        main_event = None

    html = render('event.html', main_event=main_event, rest_events=events)
    return {'html': html}

if __name__ == '__main__':
    print aws_func(None, None)['html']


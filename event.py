from facebook import GraphAPI
import requests
import arrow
import re

from renderer import render

import config

graph = GraphAPI(access_token=config.ACCESS_TOKEN, version="2.5")

def get_latest_event_raw():
    id = config.EVENT_PAGE + "/events"
    return graph.get_object(
        id,
        limit=1,
        fields="id,name,start_time,attending_count,interested_count"
    )


EVENT_PICTURE_RE = re.compile('coverPhotoImg(.*?)src="([^"]+)')

def get_full_event_picture(url):
    res = requests.get(url)
    match = EVENT_PICTURE_RE.search(res.text)
    if match is None:
        return None
    else:
        return match.group(2).replace('&amp;', '&')

class Event(object):
    def __init__(self, obj):
        data = obj['data'][0]
        self.id = data['id']
        self.url = u"https://www.facebook.com/events/" + self.id
        self.name = data['name']
        self.start_time = arrow.get(data['start_time'])
        self.attending_count = data['attending_count']
        self.interested_count = data['interested_count']

def get_latest_event():
    event = Event(get_latest_event_raw())
    event.picture_url = get_full_event_picture(event.url)
    return event

def aws_func(event, context):
    event = get_latest_event()
    html = render('event.html', event=event)
    return {'html': html}

if __name__ == '__main__':
    print aws_func(None, None)['html']


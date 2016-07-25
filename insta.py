import requests
import re

import config

CODE_RE = re.compile('"code":\s*"([^"]+)"')

def get_latest_image_code():
    url = 'https://www.instagram.com/' + config.INSTAGRAM_USER
    text = requests.get(url).text
    match = CODE_RE.search(text)
    if match is not None:
        return match.group(1)

OEMBED_API = "https://api.instagram.com/oembed"

def get_embed_code(code):
    insta_url = "http://instagr.am/p/" + code
    res = requests.get(OEMBED_API, params={'url': insta_url})
    return res.json()['html']

def aws_func(event, context):
    code = get_latest_image_code()
    html = get_embed_code(code)
    return {'html': html}

if __name__ == '__main__':
    print aws_func(None, None)['html']


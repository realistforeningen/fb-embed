import requests
from http.server import BaseHTTPRequestHandler
import re

import renderer
import config

CODE_RE = re.compile('"shortcode":\s*"([^"]+)"')

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

def fetch_and_render():
    code = get_latest_image_code()
    html = get_embed_code(code)
    html += "<script>" + renderer.files['autoheight.js'] + "</script>"
    return html

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-control', 's-maxage=600, stale-while-revalidate')
        self.end_headers()
        self.wfile.write(fetch_and_render().encode())

if __name__ == '__main__':
    print(fetch_and_render())

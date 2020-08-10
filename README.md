# embed

This is a project which builds embeddable iframes which presents data
from Facebook/Instagram. It's designed to work as a library or run within Vercel.

## Getting started

Install dependencies:

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Set an access token:

```
$ export FACEBOOK_ACCESS_TOKEN=…
```

See the generated HTML:

```
$ python fb.py
$ python insta.py
```

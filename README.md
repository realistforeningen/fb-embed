# embed

This is a project which builds embeddable iframes which presents data
from Facebook/Instagram. It's designed to work as a library or run within AWS
Lambda.

## Getting started

Install dependencies:

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Create a `config.py`:

```python
ACCESS_TOKEN = '...'

EVENT_PAGE = 'realistforeningen'
INSTAGRAM_USER = 'rf_uio'
```

See the generated HTML:

```
$ python event.py
```

## Deploy to Lambda

This project ships with a `event.json` which can be used by
`lambda-uploader` to upload the projet to AWS Lambda.

```
$ pip install lambda-uploader
$ lambda-uploader -c event.json
```




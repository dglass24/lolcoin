from random import randint
import requests
import time
import json

GET = 'get'
POST = 'post'

def get(url):
    response = requests.get(url).content
    return response

def post(url, data=None):
    if data:
        try:
            json.loads(data) # data is already json
        except:
            data = json.dumps(data) # data is not json

        response = requests.post(url, json=data).content
    else:
        response = requests.post(url).content

    return response


def request(type, url, data=None):
    """
    This function will try to make a request 3 times to the url provided. If there is an
    issue with the request the function will sleep for up to 3 seconds before trying again.
    """
    response = None
    success = False
    tries = 3
    while not success and tries > 0:
        try:
            if type is GET:
                response = get(url)
            elif type is POST:
                response = post(url, data)

            success = True
        except:
            time.sleep(randint(1, 3))

        tries -= 1

    return response
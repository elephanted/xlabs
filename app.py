#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "floatGetPerson":
        req2 = floatGetPersonQ(req)
        return req2
    elif req.get("result").get("action") == "getUserFloat":
        req2 = getUserFloatQ(req)
        return req2
    elif req.get("result").get("action") == "getUserTasksToday":
        req2 = getUserTasksToday(req)
        return req2
    else:
        return {
            "speech": "whoops",
            "displayText": "whoopsie",
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

def floatGetPersonQ(req):
    q = Request("https://api.float.com/api/v1/people/305506")
    q.add_header("Authorization", "c40733f4f634d7063e1c1beaa3beb263abf319df")
    a = urlopen(q).read()
    data = json.loads(a)
    res = makeWebhookResult(data)
    return res

def getUserFloatQ(req):
    result = req.get("result")
    parameters = result.get("parameters")
    user_id = parameters.get("phone-number")
    url = "https://api.float.com/api/v1/people/" + user_id

    q = Request(url)
    q.add_header("Authorization", "c40733f4f634d7063e1c1beaa3beb263abf319df")
    a = urlopen(q).read()
    data = json.loads(a)

    res = makeWebhookResult(data)
    return res

def getUserTasksToday(req):
    result = req.get("result")
    parameters = result.get("parameters")
    user_id = parameters.get("last-name")
    url = "https://api.float.com/api/v1/tasks?people_id=" + user_id

    q = Request(url)
    q.add_header("Authorization", "c40733f4f634d7063e1c1beaa3beb263abf319df")
    a = urlopen(q).read()
    data = json.loads(a)

    res = makeWebhookResultTask(data)
    return res

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    u_name = data.get('name')
    if u_name is None:
        return {
            "speech": "hey",
            "displayText": "hey hey",
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

    speech = "The user name is " + u_name

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def makeWebhookResultTask(data):
    try
        task = data['people'][0]['tasks'][0]['project_name']
        # hours = data['people'][0]['tasks'][0]['hours_pd']
        notes = data['people'][0]['tasks'][0]['task_notes']
        if task is None:
            return {
                "speech": "Task fail",
                "displayText": "Task fail",
                # "data": data,
                # "contextOut": [],
                "source": "apiai-weather-webhook-sample"
            }

        speech = "Today you are working on " + task + ". " + notes
    except
        speech = sys.exc_info()[0]

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

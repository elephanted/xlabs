#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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

    res = makeWebhookResultTask(data)
    return res

def getUserTasksToday(req):
    result = req.get("result")
    parameters = result.get("parameters")
    user_id = parameters.get("phone-number")
    url = "https://api.float.com/api/v1/tasks?people_id=" + user_id

    q = Request(url)
    q.add_header("Authorization", "c40733f4f634d7063e1c1beaa3beb263abf319df")
    a = urlopen(q).read()
    data = json.loads(a)

    res = makeWebhookResult(data)
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



    # query = data.get('query')
    # if query is None:
    #     return {}
    #
    # result = query.get('results')
    # if result is None:
    #     return {}
    #
    # channel = result.get('channel')
    # if channel is None:
    #     return {}
    #
    # item = channel.get('item')
    # location = channel.get('location')
    # units = channel.get('units')
    # if (location is None) or (item is None) or (units is None):
    #     return {}
    #
    # condition = item.get('condition')
    # if condition is None:
    #     return {}
    #
    # # print(json.dumps(item, indent=4))
    #
    # speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
    #          ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

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
    task-obj = data.get(0)
    if taskQ is None:
        return {
            "speech": "Task fail",
            "displayText": "Task fail",
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }
    taskName = taskobj.get("name")
    if taskName is None:
        return {
            "speech": "Task name fail",
            "displayText": "Task name fail",
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }
    speech = "The task is " + TaskName

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

def getPeopleHarvest(req):
    try:
        # result = req.get("result")
        # username = "pescettoe@amvbbdo.com"
        # password = "Welcome1!"
        # top_level_url = "https://xlaboration.harvestapp.com/people/1514150"
        #
        # # create an authorization handler
        # p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # p.add_password(None, top_level_url, username, password);
        # auth_handler = urllib.request.HTTPBasicAuthHandler(p)
        # opener = urllib.request.build_opener(auth_handler)
        # opener.addheaders = [("Authorization", "Basic cGVzY2V0dG9lQGFtdmJiZG8uY29tOldlbGNvbWUxIQ==")]
        # opener.addheaders = [("Accept", "application/json")]
        # opener.addheaders = [("Content-Type", "application/json")]
        # # opener.add_header("Accept", "application/json")
        # # opener.add_header("Content-Type", "application/json")
        # urllib.request.install_opener(opener)
        # result = opener.open(top_level_url)
        # a = result.read()
        # data = json.loads(a)
        # res = makeWebhookHarvestPeople(data)
        # return res

        q = Request("https://xlaboration.harvestapp.com/people/1514150")
        q.add_header("Authorization", "Basic cGVzY2V0dG9lQGFtdmJiZG8uY29tOldlbGNvbWUxIQ==")
        q.add_header("Accept", "application/json")
        q.add_header("Content-Type", "application/json")
        a = urlopen(q).read()
        data = json.loads(a)
        res = makeWebhookResult(data)
        return res

    except:
        speech = sys.exc_info()[0]
        displayText = traceback.print_exc()
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": displayText,
            # "data": data,
            # "contextOut": [],
            "source": "apiai-weather-webhook-sample"
        }

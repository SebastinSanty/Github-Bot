import requests
import cherrypy
import json
import re
from lxml import html


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
    	cl = cherrypy.request.headers['Content-Length']
    	resp = cherrypy.request.body.read(int(cl)).decode('utf-8')
    	jsondata = json.loads(resp)
    	print(json.dumps(jsondata, indent=4, sort_keys=True))
    	m =[]
    	if (jsondata["action"] == "created"):
    		m = re.finditer('[Bb][Uu][Gg]\s*[0-9]+', jsondata["comment"]["body"])
    	elif (jsondata["action"] == "opened"):
    		m = re.finditer('[Bb][Uu][Gg]\s*[0-9]+', jsondata["issue"]["body"] + jsondata["issue"]["title"])
    	md = '' 
    	for i in m:
    		page = requests.get('https://bugzilla.mozilla.org/rest/bug/' + re.search(r'\d+', i.group()).group())
    		if 'error' not in page.json():
    			status = page.json()["bugs"][0]["status"] + " " + page.json()["bugs"][0]["resolution"]
    			component = page.json()["bugs"][0]["component"]
    			summary = page.json()["bugs"][0]["summary"]
    			print(i.group(), status)
    			md = md + summary +"<br/>![Status](https://img.shields.io/badge/Status-" + status + "-blue.svg?style=flat) ![Status](https://img.shields.io/badge/Component-" + component + "-green.svg?style=flat) <br /> [https://bugzil.la/" + re.search(r'\d+', i.group()).group() + "](https://bugzil.la/" + re.search(r'\d+', i.group()).group() + ")<br /> ------ <br/>"
    	if (jsondata["sender"]["url"] != "https://api.github.com/users/mozilla-bot"):
    		response = requests.post(jsondata["issue"]["url"] + "/comments",headers={'Authorization': ''}, json={"body": md})

    	return "Hello world!"

if __name__ == '__main__':
   cherrypy.quickstart(HelloWorld())



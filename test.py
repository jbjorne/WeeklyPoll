# -*- coding: utf-8 -*-

import urllib
import time
from splinter import Browser

# args = [("type","date"), 
#         ("title","Floorball"), 
#         ("name","Jari Bjorne"), 
#         ("eMailAddress","jari.bjorne@utu.fi")]
#
DATA = {
        "name":"Jari",
        "email":"jari.bjorne@utu.fi",
        "title":"Floorball",
        "20090703":"1500"}

url = "http://doodle.com/create?"
url += "&".join([key + "=" + urllib.quote(DATA[key]) for key in DATA.keys()])
url += "&20090703=815&"
print url

browser = Browser()
browser.visit(url)
labels = {}
#print browser.find_by_tag("value")
#print browser.find_by_tag("input")
for label in browser.find_by_tag("label"):
    labels[label.text] = label["for"]
inputs = {}
for input in browser.find_by_tag("input"):
    inputs[input["id"]] = input

# Add the email to the form (would requirea POST request with HTML arguments)
inputs[labels["E-mail address"]].fill(DATA["email"])

browser.find_by_value('Next')[0].click()
time.sleep(3)
browser.find_by_value('Next')[0].click()
time.sleep(3)
browser.find_by_value('Next')[0].click()

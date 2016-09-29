# -*- coding: utf-8 -*-

import urllib
import time
from splinter import Browser

# args = [("type","date"), 
#         ("title","Floorball"), 
#         ("name","Jari Bjorne"), 
#         ("eMailAddress","jari.bjorne@utu.fi")]
# 
# url = u"http://doodle.com/create?"
# url += "&".join([x[0] + "=" + urllib.quote(x[1]) for x in args[0:3]])
# url += "&20090703=815&"
# url += "&".join([x[0] + "=" + urllib.quote(x[1]) for x in args[3:]])

DATA = {
        "name":"Jari",
        "email":"jari.bjorne@utu.fi",
        "title":"Floorball",
        "date":"20090703",
        "time":"1500"}

url = "http://doodle.com/create"
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

inputs[labels["Title"]].fill(DATA["title"])
inputs[labels["Your name"]].fill(DATA["name"])
inputs[labels["E-mail address"]].fill(DATA["email"])
#print browser.find_by_value('Next')

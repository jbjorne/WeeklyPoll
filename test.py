# -*- coding: utf-8 -*-

import urllib
import time
from splinter import Browser

def clickButton(browser, label):
    buttons = browser.find_by_value(label)
    print buttons
    clicked = False
    for button in buttons:
        try:
            button.click()
            clicked = True
        except:
            pass
    if not clicked:
        raise Exception("Button " + label + "not found")

# args = [("type","date"), 
#         ("title","Floorball"), 
#         ("name","Jari Bjorne"), 
#         ("eMailAddress","jari.bjorne@utu.fi")]
#
DATA = {
        "name":"Jari",
        "email":"floorball_admin@mailinator.com",
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

buttonLabels = 4 * ["Next"] + ["Finish"]
for label in buttonLabels: 
    clickButton(browser, label)

link = browser.find_by_name("participationLink")
print "Link:", link["href"]

adminLink = browser.find_by_name("adminLink")
browser.visit(adminLink["href"] + "#notifications")
browser.uncheck("followEvents")
browser.find_by_id("saveNotifications")[0].click()
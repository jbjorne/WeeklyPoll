# -*- coding: utf-8 -*-

import urllib
import datetime
from splinter import Browser
import json

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
# DATA = {
#         "name":"Jari",
#         "email":"floorball_admin@mailinator.com",
#         "title":"Floorball",
#         "20090703":"1500"}

def addVar(url, name, value):
    return url + "&" + name + "=" + urllib.quote(value)

def makeDoodle(title, name, email, dates):
    url = "http://doodle.com/create?"
    url = addVar(url, "title", title)
    url = addVar(url, "name", name)
    for date in dates.keys():
        url += "&" + date + "=" + dates[date]
    print url
    
    browser = Browser()
    browser.visit(url)
    labels = {}
    for label in browser.find_by_tag("label"):
        labels[label.text] = label["for"]
    inputs = {}
    for input in browser.find_by_tag("input"):
        inputs[input["id"]] = input
    
    # Add the email to the form (would requirea POST request with HTML arguments)
    inputs[labels["E-mail address"]].fill(email)
    
    buttonLabels = 4 * ["Next"] + ["Finish"]
    for label in buttonLabels: 
        clickButton(browser, label)
    
    link = browser.find_by_name("participationLink")["href"]
    print "Link:", link
    adminLink = browser.find_by_name("adminLink")["href"]
    browser.visit(adminLink + "#notifications")
    browser.uncheck("followEvents")
    browser.find_by_id("saveNotifications")[0].click()
    
    browser.quit()
    return link, adminLink

def makeDoodleForDate(title, name, email, date, time):
    return makeDoodle(title, name, email, {date.strftime("%Y%m%d"):time})

def getDates(weekday, fromDate, toDate):
    days = [fromDate + datetime.timedelta(x) for x in range(int ((toDate - fromDate).days))]
    days = [x for x in days if x.weekday() == weekday]
    #print days #weekday, [x.weekday() for x in days]
    return days

def makeDoodles(title, name, email, weekday, time, begin, end, dummy, output):
    dates = getDates(weekday, datetime.datetime.strptime(begin, "%Y%m%d"), datetime.datetime.strptime(end, "%Y%m%d"))
    print dates
    data = []
    for date in dates:
        print "Making poll for date", date
        link, adminLink = None, None
        if not dummy:
            link, adminLink = makeDoodleForDate(title, name, email, date, time)
        data.append({"date":date.strftime("%Y%m%d"), "link":link, "adminLink":adminLink, "weekday":weekday, "time":time, "title":title, "email":email})
    if len(data) > 0 and output != None:
        with open(output, 'w') as fp:
            json.dump(data, fp)
    
if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser(description="Batch process a tree of input files")
    optparser.add_option("-l", "--title", default=None)
    optparser.add_option("-n", "--name", default=None)
    optparser.add_option("-m", "--email", default=None)
    optparser.add_option("-w", "--weekday", type=int, default=None)
    optparser.add_option("-t", "--time", default=None)
    optparser.add_option("-b", "--begin", default=None)
    optparser.add_option("-e", "--end", default=None)
    optparser.add_option("-d", "--dummy", default=False, action="store_true")
    optparser.add_option("-o", "--output", default=None)
    (options, args) = optparser.parse_args()
    
    makeDoodles(options.title, options.name, options.email, options.weekday, options.time, options.begin, options.end, options.dummy, options.output)
    
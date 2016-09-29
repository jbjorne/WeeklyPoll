# -*- coding: utf-8 -*-

import urllib
import datetime
from splinter import Browser
import json
import time

def clickButton(browser, label):
    buttons = browser.find_by_value(label)
    clicked = False
    for button in buttons:
        try:
            button.click()
            clicked = True
        except:
            pass
    if not clicked:
        raise Exception("Button " + label + "not found")

def addVar(url, name, value):
    return url + "&" + name + "=" + urllib.quote(value)

def makeDoodle(title, name, email, dates):
    # Define the Doodle Poll Wizard URL and prefill as many fields as possible
    url = "http://doodle.com/create?"
    url = addVar(url, "title", title)
    url = addVar(url, "name", name)
    for date in dates.keys():
        url += "&" + date + "=" + dates[date]
    print url
    
    # Start the browser and go to the URL
    browser = Browser()
    browser.visit(url)
    
    # Collect input elements
    labels = {}
    for label in browser.find_by_tag("label"):
        labels[label.text] = label["for"]
    inputs = {}
    for input in browser.find_by_tag("input"):
        inputs[input["id"]] = input
    
    # Add the email to the form (would require a POST request with HTML arguments)
    inputs[labels["E-mail address"]].fill(email)
    
    # Click through the pre-filled poll configuration pages
    buttonLabels = 4 * ["Next"] + ["Finish"]
    for label in buttonLabels: 
        clickButton(browser, label)
    
    # Once the poll has been generated, save the link
    link = None
    while link == None: # Wait for the poll to be generated
        try:
            link = browser.find_by_name("participationLink")
        except:
            print "Waiting for the link"
            link = None
            time.sleep(1)
    link = link["href"]
    print "Link:", link
    # Get the admin link for the poll
    adminLink = browser.find_by_name("adminLink")["href"]
    # Disable poll notification emails
    browser.visit(adminLink + "#notifications")
    browser.uncheck("followEvents")
    browser.find_by_id("saveNotifications")[0].click()
    
    browser.quit()
    return link, adminLink

def makeDoodleForDate(title, name, email, date, timeOfDay):
    return makeDoodle(title, name, email, {date.strftime("%Y%m%d"):timeOfDay})

def getDates(weekday, fromDate, toDate):
    # Get all dates corresponding to a weekday in a defined range
    days = [fromDate + datetime.timedelta(x) for x in range(int ((toDate - fromDate).days))]
    days = [x for x in days if x.weekday() == weekday]
    return days

def makeDoodles(output, title, name, email, weekday, timeOfDay, begin, end, dummy):
    dates = getDates(weekday, datetime.datetime.strptime(begin, "%Y%m%d"), datetime.datetime.strptime(end, "%Y%m%d"))
    print dates
    data = []
    for date in dates:
        print "Making poll for date", date
        link, adminLink = None, None
        if not dummy:
            weekdays = {0:"Mo", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}
            fullTitle = title + " ".join(["", weekdays[weekday], date.strftime("%d.%m.%Y"), "at", timeOfDay[0:2] + ":" + timeOfDay[2:]])
            link, adminLink = makeDoodleForDate(fullTitle, name, email, date, timeOfDay)
        data.append({"date":date.strftime("%Y%m%d"), "link":link, "adminLink":adminLink, "weekday":weekday, "time":timeOfDay, "title":fullTitle, "email":email})
    if len(data) > 0 and output != None:
        with open(output, 'w') as fp:
            json.dump(data, fp)
    
if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser(description="Make a doodle for a recurring event")
    optparser.add_option("-l", "--title", default=None, help="The poll title (time and date will be added to this automatically)")
    #optparser.add_option("--extendTitle", default=False, action="store_true")
    optparser.add_option("-n", "--name", default=None, help="Poll author's name")
    optparser.add_option("-m", "--email", default=None, help="Poll author's email")
    optparser.add_option("-w", "--weekday", type=int, default=None, help="The day of week for the poll. Format as YYYYMMDD")
    optparser.add_option("-t", "--time", default=None, help="The time point during the day of week. Format as HHMM.")
    optparser.add_option("-b", "--begin", default=None, help="The begin date for the date range for which polls are generated. Format YYYMMDD.")
    optparser.add_option("-e", "--end", default=None, help="The end date for the date range for which polls are generated. Format YYYMMDD.")
    optparser.add_option("-d", "--dummy", default=False, action="store_true", "Dummy mode for testing. No polls are generated.")
    optparser.add_option("-o", "--output", default=None)
    (options, args) = optparser.parse_args()
    
    makeDoodles(options.output, options.title, options.name, options.email, options.weekday, options.time, options.begin, options.end, options.dummy)
    
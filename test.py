# -*- coding: utf-8 -*-

import urllib
from splinter import Browser

args = {
        "type":"date",
        "title":"Floorball",
        "name":u"Jari Bjorne",
        "eMailAddress":"jari.bjorne@utu.fi"}

url = u"http://doodle.com/create?"
url += "&".join([key + "=" + urllib.quote(args[key]) for key in sorted(args.keys())])
url += "&20090703=815"

print url

browser = Browser()
browser.visit(url)

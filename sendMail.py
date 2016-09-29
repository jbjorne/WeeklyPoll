import json
import datetime
import subprocess
import codecs

def readEmails(emailPath):
    with codecs.open(emailPath, "rt", "utf-8") as f:    
        emails = f.read()
    emails.replace("\n", " ").strip()
    emails = emails.split(",")
    data = []
    for email in emails:
        name, address = email.split("<")
        name = name.strip()
        address = address.replace(">", "").strip()
        print name, address
        data.append({"name":name, "email":address})
    return data

def runMailCommand(doodle, recipients, template, dummy):
    command = u"mail -s '" + doodle["title"] + "'"
    for recipient in recipients:
        if recipient["name"] != None:
            command += " '" + recipient["name"] + " <" + recipient["email"] + ">'"
        else:
            command += " " + recipient["email"]
    print "--------------------------"
    print command
    print "--------------------------"
    template = template.replace("%doodle", doodle["link"])
    print template
    print "--------------------------"
    if not dummy:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.communicate(input=template)

def sendMail(doodlesPath, emailPath, daysInAdvance, templatePath, dummy=False):
    emails = readEmails(options.emails)
    
    with open(doodlesPath) as f:    
        doodles = json.load(f)
    
    with codecs.open(templatePath, "rt", "utf-8") as f:    
        template = f.read()
    
    today = datetime.datetime.today()
    print "Current time is", today
    for doodle in doodles:
        print "Checking", doodle,
        sent = doodle.get("sent")
        if sent == True:
            print "already sent"
            continue
        if sent == None:
            doodle["sent"] = False
        date = datetime.datetime.strptime(doodle["date"], "%Y%m%d")
        delta = date - today
        if delta.days <= daysInAdvance:
            print "Sending email now"
            runMailCommand(doodle, emails, template, dummy)
            if not dummy:
                doodle["sent"] = True
        else:
            print "checked, delta is", delta
    
    with open(doodlesPath, 'w') as fp:
        json.dump(doodles, fp)

if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser(description="Sends a notification email with a Doodle link.")
    optparser.add_option("-l", "--doodles", default=None, help="JSON-formatted file of pre-generated Doodle links made with makeDoodles.py")
    optparser.add_option("-m", "--emails", default=None, help="Recipient email addresses (comma separated list, either of the form 'Name <name@domain.com>' or just 'name@domain.com')")
    optparser.add_option("-t", "--template", default=None, help="Email body. The string '%doodle' will be replaced with the corresponding Doodle link")
    optparser.add_option("-s", "--days", type=int, default=None, help="How many days in advance to send the notification email")
    optparser.add_option("-d", "--dummy", default=False, action="store_true", help="Don't send the mail, just print it on screen")
    (options, args) = optparser.parse_args()
    
    #sendMail = readEmails(options.emails)
    sendMail(options.doodles, options.emails, options.days, options.template, options.dummy)
    
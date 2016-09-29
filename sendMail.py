import json
import datetime
import subprocess

def readEmails(emailPath):
    with open(emailPath) as f:    
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

def runMailCommand(doodle, recipients, template):
    command = "mail -s " + doodle["fullTitle"]
    for recipient in recipients:
        if recipient["name"] != None:
            command += "'" + recipient["name"] + " <" + recipient["email"] + ">"
    print command
    template = template.replace("%doodle", doodle["link"])
    print template
    #p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    #return p.communicate(input=content)

def sendMail(doodlesPath, emailPath, daysInAdvance, teplatePath):
    emails = readEmails(options.emails)
    
    with open(doodlesPath) as f:    
        doodles = json.load(f)
    
    today = datetime.datetime.now()
    for doodle in doodles:
        sent = doodle.get("sent")
        if sent == None:
            doodle["sent"] = False
        date = datetime.datetime.strptime(doodle["date"], "%Y%m%d")
        delta = datetime.timedelta(today, date)
        if delta.days <= daysInAdvance:
            print "Sending email for doodle", doodle
            #doodle["sent"] = True
    
    with open(doodlesPath, 'w') as fp:
        json.dump(doodles, fp)

if __name__=="__main__":
    from optparse import OptionParser
    optparser = OptionParser(description="Batch process a tree of input files")
    optparser.add_option("-d", "--doodles", default=None)
    optparser.add_option("-m", "--emails", default=None)
    optparser.add_option("-s", "--days", type=int, default=None)
    (options, args) = optparser.parse_args()
    
    sendMail = readEmails(options.emails)
    
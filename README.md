## Weekly Doodle Poll

These scripts allow the generation of weekly Doodle polls for recurring events
such as meetings, sports practice etc. All Doodle polls for a given period are
generated in advance and their links are stored for later use. Notification 
emails are later sent with the appropriate links included.

## Generating the Doodle Polls

Recurring Doodle polls are generated with the Splinter web automation toolkit.
Splinter can be installed from PyPi as package 'splinter'.

To generate Doodle polls for the time point of 15:00 for Tuesdays between
September 20th 2016 and October 20th 2016 the following command can be used:

`python makeDoodles.py -b 20160920 -e 20161020 -w 1 -t 1500 -n "Owner" -m "owner@domain.com" -o doodles.json -l "Title"`

Links for the generated Doodle polls will be saved to the output file defined
with the -o argument.

## Sending Notification Emails

Notification emails can be sent closer to the actual event using the sendMail.py
command. This program depends on the UNIX 'sendmail' utility which must be installed
and configured on the computer the command is run, if the command is run in non-dummy
mode. To send notifications one day in advance for the polls generated in the previous 
step, the following command can be used:

`python sendMail.py -l doodles.json -m emails.txt -t template.txt -s 1`

The program will read the doodles.json file and send a notification email for each poll
whose due date is within the range defined with the -s switch. Additionally, sendMail.py
will save the 'sent' state for each Doodle poll defined in doodles.json, so even if the
program is run twice, an already sent notification will not be resent.

The email addresses are read from the file defined with the -m switch. The addresses are
saved in the standard email "To:" field format.

The actual message is customized based on the file defined with the -s switch. The template
follows the sendmail template format with a few customizable wildcards. The standard
strftime arguments can be used to insert poll date information into the mail. The
string '%doodle' will be replaced with a link to the relevant Doodle poll and the string
'%recipients' with the list of email adresses defined with the -m switch. For example, the 
following template could be used for emails:

```
From: fromaddress@domain.com
To: %recipients
Subject: Event at %Y/%m/%d at %H:%M

Hi,

Please tell if you will be attending my event: %doodle

Cheers,
Pollster
```

## Automating Notification Emails

The sending of notification emails with sendMail.py can be automated e.g. with a cron job. 
The cron job can be run once per day, and sendMails.py will then send notifications for
all Doodle's within the due date range.
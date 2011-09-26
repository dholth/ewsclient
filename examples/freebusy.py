#!/usr/bin/env python
"""
Fetch free/busy information.
"""

import ewsclient
import ewsclient.monkey
import datetime
import os
import sys
import suds.client
import logging
from suds.transport.https import WindowsHttpAuthenticated

logging.basicConfig(level=logging.DEBUG)

email = sys.argv[1]

domain = os.environ.get('EWS_DOMAIN')
username = os.environ.get('EWS_USER')
password = os.environ.get('EWS_PASS')

transport = WindowsHttpAuthenticated(username=username,
        password=password)
client = suds.client.Client("https://%s/EWS/Services.wsdl" % domain,
        transport=transport,
        plugins=[ewsclient.AddService()])

tz = client.factory.create('t:TimeZone')

tz.Bias = 300

tz.StandardTime.Bias = 0
tz.StandardTime.Time = '02:00:00'
tz.StandardTime.DayOrder = 1
tz.StandardTime.Month = 11
tz.StandardTime.DayOfWeek = 'Sunday'

tz.DaylightTime.Bias = -60
tz.DaylightTime.Time = '02:00:00'
tz.DaylightTime.DayOrder = 2
tz.DaylightTime.Month = 3
tz.DaylightTime.DayOfWeek = 'Sunday'

md = client.factory.create('MailboxDataArray')

mde = client.factory.create('t:MailboxData')
mde.Email.Address = email
mde.AttendeeType = 'Room'
mde.ExcludeConflicts = 'false'
md.MailboxData.append(mde)

fb = client.factory.create('t:FreeBusyViewOptions')
fb.TimeWindow.StartTime = datetime.datetime.now().isoformat()
fb.TimeWindow.EndTime = (datetime.datetime.now() +
        datetime.timedelta(hours=12)).isoformat()
fb.MergedFreeBusyIntervalInMinutes = 60
fb.RequestedView = 'DetailedMerged'

print client.service.GetUserAvailability(tz, md, fb)

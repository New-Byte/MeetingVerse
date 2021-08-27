from O365 import Account, MSGraphProtocol
import datetime as dt
import sys
from random import randint

args = sys.argv

CLIENT_ID = '943a666e-3ab7-4d1c-9e24-7c61289594c4'
SECRET_ID = '5z-Wknt_6-B9dnn6.v.5gaAiW3Dc-jmS84'

credentials = (CLIENT_ID, SECRET_ID)
protocol = MSGraphProtocol() 

#protocol = MSGraphProtocol(defualt_resource='<sharedcalendar@domain.com>') 
scopes = ['Calendars.Read.Shared','Calendars.ReadWrite.Shared']
account = Account(credentials, protocol=protocol)

if account.authenticate(scopes=scopes):
   print('Authenticated!')

schedule = account.schedule()
calendar = schedule.get_default_calendar()

q = calendar.new_query('start').greater_equal(dt.datetime(2021, 8, 1))
q.chain('and').on_attribute('end').less_equal(dt.datetime(2021, 8, 31))


events = calendar.get_events(include_recurring=False) 
#events = calendar.get_events(query=q, include_recurring=True) 

for event in events:
    print(event)

new_event = calendar.new_event()  # creates a new unsaved event 
new_event.subject = args[1]
new_event.location = "Work From Home"
new_event.is_online_meeting = True
new_event.online_meeting_provider = 'teamsForBusiness'
#new_event.organizer = ''
new_event.weblink = "https://teams.live.com/meet/" + str(randint(10**14,10**15-1))
new_event.attendees.add((args[2], args[3]))

new_event.start = dt.datetime(int(args[4]), int(args[5]), int(args[6]), int(args[7]), int(args[8]))
new_event.end = dt.datetime(int(args[4]), int(args[5]), int(args[6]),int(args[9]), int(args[10]))
#new_event.recurrence.set_daily(1, end=dt.datetime(int(args[4]), int(args[5]), int(args[6]),int(args[9]), int(args[10])))
new_event.remind_before_minutes = 45

new_event.save()
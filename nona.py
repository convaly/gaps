
from gocal import GCalendar
c=GCalendar()
c.setup()
c.callapi()
a='test'
s='2018-07-28T09:00:00-07:00'
e='2018-07-28T17:00:00-07:00'
c.addEvent(a,s,e)
from datetime import datetime
from datetime import timedelta

from gocal import GCalendar


def get_events(c):
    all_raw_events = c.get_raw_events()
    b, split, matrix = [], [], []
    date = datetime.date(datetime.today())
    j = 0
    next_day = False
    while j < len(all_raw_events):
        if ((str(all_raw_events[j].get('start')))[14:24]) == str(date):
            b.append(all_raw_events[j])
            j = j + 1
            next_day = True
        if not next_day or j == len(all_raw_events):
            date = date + timedelta(days=1)
            matrix.append(b[:])
            for i in range(0, len(b)):
                if ((str(b[i].get('end')))[14:24]) == str(date):
                    split.append(b[i])
            b.clear()
            b += split
            split.clear()
        next_day = False
    if len(b) != 0:
        matrix.append(b)
    return matrix


def to_just_names(full_table):
    small_table = []
    table = []
    for k in range(0, len(full_table)):
        for l in range(0, len(full_table[k])):
            small_table.append(full_table[k][l].get('summary'))
        table.append(small_table[:])
        small_table.clear()
    return table


# start
c = GCalendar()
c.start()
t = get_events(c)
print(to_just_names(t))


a = 'dupa'
s = '2018-08-01T07:30:00+01:00'
e = '2018-08-01T15:00:00+01:00'
# c.addEvent(a,s,e)

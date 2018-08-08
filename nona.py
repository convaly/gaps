from datetime import datetime
from datetime import timedelta
from gocal import GCalendar
from gotasks import GTasksContainer
from tzlocal import get_localzone

def get_events(clndr):
    all_raw_events = clndr.get_raw_events()
    b, split, matrix = [], [], []
    date = datetime.date(datetime.today())
    j = 0
    next_day = False
    while j < len(all_raw_events):
        try:
            evntdate = datetime.date(datetime.strptime(str(all_raw_events[j].get('start'))[14:24], '%Y-%m-%d'))
        except:
            evntdate = datetime.date(datetime.strptime(str(all_raw_events[j].get('start'))[10:20], '%Y-%m-%d'))
        if evntdate == date:
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
        matrix.append(b[:])
    return matrix


def extract_single_attribute(full_table, attribute):
    small_table = []
    table = []
    for k in range(0, len(full_table)):
        for l in range(0, len(full_table[k])):
            small_table.append(full_table[k][l].get(attribute))
        table.append(small_table[:])
        small_table.clear()
    return table


def get_free_time(clndr):
    busy_time = get_events(clndr)
    free_time = []
    free_time_day = []
    free_time_block = {}
    local_tz = get_localzone()
    free_time_block['start'] = free_time_block['end'] = datetime.now(local_tz)
    for day in range(0, len(busy_time)):
        for event in range(0, len(busy_time[day])):
            if (datetime.strptime(str(busy_time[day][event]['start'])[14:39], '%Y-%m-%dT%H:%M:%S%z'))\
                                                  > free_time_block['start']:
                free_time_block['end'] = datetime.strptime(str(busy_time[day][event]['start'])[14:39],
                                                           '%Y-%m-%dT%H:%M:%S%z')
                free_time_block['duration'] = free_time_block['end'] - free_time_block['start']
                free_time_day.append(free_time_block.copy())
                free_time_block['start'] = free_time_block['end'] + (datetime.strptime(str(busy_time[day][event]['end'])[14:39], '%Y-%m-%dT%H:%M:%S%z') - datetime.strptime(str(busy_time[day][event]['start'])[14:39], '%Y-%m-%dT%H:%M:%S%z'))
            else:
                free_time_block['start'] = datetime.strptime(str(busy_time[day][event]['end'])[14:39], '%Y-%m-%dT%H'
                                                                                                       ':%M:%S%z')
        free_time.append(free_time_day[:])

        free_time_day.clear()
    return free_time


def allocate_event(clndr, task_container):
    events = get_events(clndr)
    tasks_to_be_allocated = task_container.get_raw_tasks()
    #dated tasks
    day=datetime.date(datetime.strptime())
    for event in range(0, len(events[day])):
        if events[1][0].get('start') <0:
            print('lol')


# start
c = GCalendar()
t = GTasksContainer()
t.get_raw_tasks()

a = get_free_time(c)

print(extract_single_attribute(a, 'duration'))

#debugging
# print(extract_single_attribute(get_free_time(c), 'start'))
# print(get_free_time(c))

# a = 'dupa'
# s = '2018-08-01T07:30:00+01:00'
# e = '2018-08-01T15:00:00+01:00'
# c.addEvent(a,s,e)

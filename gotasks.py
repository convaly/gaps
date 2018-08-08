# Google tasks class
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from pytimeparse.timeparse import timeparse
from datetime import timedelta



class GTasksContainer:
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/tasks'
        store = oauth_file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials_tasks.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('tasks', 'v1', http=creds.authorize(Http()))

    @staticmethod
    def get_duration(task):
        duration = timedelta(seconds=timeparse(task['notes'].split('\n')[0]))
        return duration

    @staticmethod
    def sort(unsorted_tasks):
        sorted_tasks = []
        tasks_with_date = []
        tasks_with_no_date = []
        i = 0
        while i < len(unsorted_tasks):
            if unsorted_tasks[i].get('due') is not None:
                tasks_with_date.append(unsorted_tasks[i])
            else:
                tasks_with_no_date.append(unsorted_tasks[i])
            i += 1
        tasks_with_date = sorted(tasks_with_date, key=lambda k: k['due'])
        sorted_tasks.append(tasks_with_date)
        sorted_tasks.append(tasks_with_no_date)
        return sorted_tasks

    def get_raw_tasks(self):
        # results = self.service.tasklists().list().execute()
        # items = results.get('items', [])
        # if not items:
        #     print('No task lists found.')
        # else:
        #     print('Task lists:')
        #     for item in items:
        #         print(u'{0} ({1})'.format(item['title'], item['id']))
        #
        task_results = self.service.tasks().list(tasklist='@default').execute()
        tasks = task_results.get('items', [])
        for task in tasks:
            try:
                task['duration'] = self.get_duration(task)
            except:
                task['duration'] = -1
        tasks = self.sort(tasks)
        return tasks

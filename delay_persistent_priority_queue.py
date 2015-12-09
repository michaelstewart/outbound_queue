#!/usr/bin/python

from persistent_priority_queue import PersistentPriorityQueue
import pickle
import datetime

class DelayPersistentPriorityQueue(object):

    def __init__(self, filename=None):
        self.filename = filename
        self.available_queue = PersistentPriorityQueue()
        # queue for tasks that have a delay
        self.wait_queue = PersistentPriorityQueue()

    def put(self, message, priority=0, delay=0):
        if delay == 0:
            # No delay, message is immediately available
            self.put_in_avail(message, priority)
        else:
            self.put_in_wait(message, delay, priority)
        # Update available queue to avoid backlog upon get.
        self.move_newly_available_messages()

    def put_in_wait(self, message, delay, priority=0):
        data = (priority, message)
        available_at = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        self.wait_queue.put(data, priority=available_at)

    def put_in_avail(self, message, priority):
        self.available_queue.put(message, priority=priority)

    def get(self):
        self.move_newly_available_messages()
        return self.available_queue.get()

    def move_newly_available_messages(self):
        ''' 
        Moves messages that should be available from the 
        wait queue to the available queue

        Called upon both gets and puts to avoid backlogs.
        '''
        now = datetime.datetime.now()
        while (self.wait_queue.next_priority() is not None 
            and self.wait_queue.next_priority() < now):
            (priority, message) = self.wait_queue.get()
            self.put_in_avail(message, priority)

    def persist(self):
        if self.filename is not None:
            with open(self.filename, 'wb') as output_file:
                pickle.dump((self.available_queue, self.wait_queue), output_file)
    


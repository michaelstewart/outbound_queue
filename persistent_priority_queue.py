#!/usr/bin/python

import itertools
from heapq import heappush, heappop
import pickle

class PersistentPriorityQueue(object):

    def __init__(self, filename=None):
        self.filename = filename
        count_start = 0 # Defaults count start
        self.q = [] # Use a list for the heapq

        if self.filename is not None:
            try:
                with open(filename, 'rb') as input_file:
                    (count_start, self.q) = pickle.load(input_file)
            except IOError:
                # Not an error, just first run where we don't have a queue.
                pass

        self.counter = self.count_iterator(start=count_start)
            

    def put(self, message, priority=0):
        message_count = next(self.counter)
        heap_entry = [priority, message_count, message]
        heappush(self.q, heap_entry)

    def get(self):
        try:
            (priority, count, message) = heappop(self.q)
            return message
        except IndexError:
            return None

    def next_priority(self):
        try:
            return self.q[0][0]
        except IndexError:
            return None

    def persist(self):
        # If the filename is None we don't persist
        if self.filename is not None:
            with open(self.filename, 'wb') as output_file:
                count_for_storage = next(self.counter)
                pickle.dump((count_for_storage, self.q), output_file)


    def count_iterator(self, start=0):
        i = start
        while True:
            yield i
            i += 1


#!/usr/bin/python

import collections
import pickle

class PersistentQueue(object):

    def __init__(self, filename=None):
        self.filename = filename
        self.q = collections.deque()
        if self.filename is not None:
            try:
                with open(filename, 'rb') as input_file:
                    self.q = pickle.load(input_file)
            except IOError:
                # Not an error, just first run where we don't have a queue.
                pass

    def persist(self):
        # If the filename is None we don't persist
        if self.filename is not None:
            with open(self.filename, 'wb') as output_file:
                pickle.dump(self.q, output_file)

    def put(self, message):
        self.q.append(message)

    def get(self):
        try:
            return self.q.popleft()
        except IndexError:
            return None



#!/usr/bin/python

import collections
from Queue import Queue
import pickle 

class PersistentQueue(object):

    def __init__(self, filename):
        self.filename = filename
        # Queue.__init__(self)
        self.q = collections.deque()

    def persist(self):
        output_file = open(self.filename, 'wb')
        pickle.dump(self, output_file)

    def put(self, data):
        # self.persist()
        self.q.append(data)

    def get(self):
        # return self.get.


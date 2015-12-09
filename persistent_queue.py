#!/usr/bin/python

from Queue import Queue

class PersistentQueue(Queue):

    def __init__(self):
        Queue.__init__(self)


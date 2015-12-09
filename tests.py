#!/usr/bin/python

import unittest
import time
import os

from persistent_queue import PersistentQueue
from persistent_priority_queue import PersistentPriorityQueue
from delay_persistent_priority_queue import DelayPersistentPriorityQueue

class TestPersistentQueue(unittest.TestCase):

    def test_queue(self):
        q = PersistentQueue()
        obj = {'test':'1'}
        q.put(obj)
        self.assertEqual(obj, q.get())

class TestPersistentPriorityQueue(unittest.TestCase):

    def test_queue(self):
        q = PersistentPriorityQueue()
        # Medium priority tasks
        obj1 = {'test':'medium_priority 1'}
        q.put(obj1, priority=10)
        obj2 = {'test':'medium_priority 2'}
        q.put(obj2, priority=10)
        # High priority tasks
        obj3 = {'test':'medium_priority 3'}
        q.put(obj3, priority=1)
        obj4 = {'test':'medium_priority 4'}
        q.put(obj4, priority=1)

        order = [obj3, obj4, obj1, obj2]
        for o in order:
            self.assertEqual(o, q.get())

class TestDelayPersistentPriorityQueue(unittest.TestCase):
    

    def test_queue(self):

        q = DelayPersistentPriorityQueue()

        # Medium priority tasks
        obj1 = {'test':'medium_priority 1'}
        q.put(obj1, priority=10)
        obj2 = {'test':'medium_priority 2'}
        q.put(obj2, priority=10)
        # High priority tasks
        obj3 = {'test':'medium_priority 3'}
        q.put(obj3, priority=1)
        obj4 = {'test':'medium_priority 4'}
        q.put(obj4, priority=1)

        # 1 second delay test
        obj5 = {'test': '1s delay, should not see'}
        q.put(obj5, priority=0, delay=1)

        # 2 second delay and different priority
        obj6 = {'test': '2s delay, comes in second'}
        q.put(obj6, priority=10, delay=2)
        obj7 = {'test': '2s delay, comes in first'}
        q.put(obj7, priority=1, delay=2)

        order = [obj3, obj4, obj1, obj2, None]
        for o in order:
            self.assertEqual(o, q.get())

        time.sleep(1)
        order = [obj5, None]
        for o in order:
            self.assertEqual(o, q.get())

        time.sleep(1)
        order = [obj7, obj6, None]
        for o in order:
            self.assertEqual(o, q.get())

    def test_persistence(self):
        FILENAME = 'test_q.p'
        q = DelayPersistentPriorityQueue(FILENAME)

        obj = {'test':'persist'}
        q.put(obj)
        q.persist()

        # Recreate the queue from disk
        q = DelayPersistentPriorityQueue(FILENAME)
        self.assertEqual(obj, q.get())

        os.remove(FILENAME)

if __name__ == '__main__':
    unittest.main()


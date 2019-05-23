"""
    description: multiprocessing event engine
"""
__author__ = 'naodongbanana'

from multiprocessing import Process, Queue
import time
import glovar

class EventEngine(object):
    def __init__(self, *args, **kwargs):
        self._eventQueue = Queue()
        self._active = False
        # {'scmlworld':[handler1, handler2]}
        self._handlers = {}
        self._processPool = []
        self._mainProcess=Process(target=self._run)

    def _run(self):
        while self._active:
            if not self._eventQueue.empty():
                event = self._eventQueue.get(block=True, timeout=1)
                self._process(event)
            else:
                pass

    def _process(self, event):
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                p = Process(target=handler, args=(event, ))
                self._processPool.append(p)
                p.start()

    def start(self):
        self._active = True
        self._mainProcess.start()

    def stop(self):
        self._active = False
        for p in self._processPool:
            p.join()
        self._mainProcess.join()

    def terminate(self):
        self._active = False
        for p in self._processPool:
            p.terminate()
        self._mainProcess.join()

    def register(self, type, handler):
        try:
            handlerList = self._handlers[type]
        except KeyError:
            handlerList = []
            self._handlers[type] = handlerList
        
        if handler not in handlerList:
            self._handlers[type].append(handler)

    def unregister(self, type, handler):
        try:
            handlerList = self._handlers[type]

            if handler in handlerList:
                handlerList.remove(handler)
                self._handlers[type].remove(handler)

            if not handlerList:
                del self._handlers[type]
        
        except KeyError:
            pass

    def sendEvent(self, event):
        self._eventQueue.put(event)

class Event(object):

    def __init__(self, type=None, *args, **kwargs):
        self.type = type
        self.dict = {}

class Public_NegmasAccount:
    
    def __init__(self, eventManager):
        self._eventManager = eventManager
        self.scmlWorld = None

    def processNewStep(self, eventType, world=None):
        event = Event(eventType)
        if world:
            event.dict['current_step'] = world.current_step
        else:
            event.dict['current_step'] = 10000
        self._eventManager.sendEvent(event)
        print('negmas process new step')

class ListenerTypeOne:
    def __init__(self, username, world_recall_reuslt):
        self._username = username
        self._world_recall_reuslt = world_recall_reuslt

    def showNewStep(self, event):
        print('{} get the result of new step'.format(self._username))
        # print('plot the result of new step {}'.format(event.dict['current_step']))
        glovar.world_recall = event.dict['current_step']
        if self._world_recall_reuslt:
            self._world_recall_reuslt.value = glovar.world_recall
            print('plot the result of new step {}'.format(self._world_recall_reuslt.value))
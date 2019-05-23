import glovar
import multiprocessing
import time
from test_drawing import *
import psutil

class RecallClockProcess(multiprocessing.Process):
    def __init__(self, interval, world_recall_reuslt):
        multiprocessing.Process.__init__(self)
        self.interval = interval
        self._world_recall = self._world_recall_fun()
        self.world_recall_reuslt = world_recall_reuslt

    def stop(self):
            print('Process suspend  id %s ' %(self.pid))
            p = psutil.Process(self.pid)
            p.suspend()

    def wake(self):
            print ('Process resume  id  %s ' %(self.pid))
            p = psutil.Process(self.pid)
            p.resume()

    def _world_recall_fun(self):
        world = 0
        while True:
            yield world
            world +=1
            
    def run(self):
        print ('当前运行进程PID :  %s  '  %self.pid) 
        while True:
            glovar.world_recall = next(self._world_recall)
            print('world_recall',glovar.world_recall)
            print("the time is {0}:world_recall_fun {1}".format(time.ctime(),glovar.world_recall))
            if self.world_recall_reuslt:
                self.world_recall_reuslt.value = glovar.world_recall
            # self.stop()
            time.sleep(self.interval)
            # self.wake()

if __name__ == '__main__':
    world_recall_reuslt = glovar.world_recall_reuslt
    fig, ax = plt.subplots(1,1) 
    p = RecallClockProcess(3, world_recall_reuslt=world_recall_reuslt)
    a = ShowProcess(ax=ax, fig=fig)
    p.start()
    a.show()
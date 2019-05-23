import glovar
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ShowProcess:
    def __init__(self, ax=None, fig=None, world_recall_reuslt_dict=None, *args, **kwargs):
        self.ax = ax
        self.fig = fig
        self.world_recall = 0
        self.iterf = self.iter_frame()
        self._world_recall_reuslt_dict = world_recall_reuslt_dict

    def iter_frame(self):
        step = 0
        step_information = 0
        while True:
            step_information = self._world_recall_reuslt_dict['current_step'] if 'current_step' in self._world_recall_reuslt_dict else 0
            yield step_information
            step +=1

    def update(self,frame):
        print('frame:' ,frame)
        scat = self.ax.scatter(frame, frame)
        return scat,

    def show(self):
        ai = FuncAnimation(self.fig, self.update, frames=self.iterf, interval=1000)
        plt.show(block = True)

if __name__ == "__main__":
    fig, ax = plt.subplots(1,1)
    a = ShowProcess(ax=ax, fig=fig)
    a.show()
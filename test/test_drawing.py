import glovar
import sys
sys.path.append('../')
import dynetx as dnx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# from threading import Event
import itertools
class ShowProcess:
    def __init__(self, ax=None, fig=None, world_recall_reuslt_dict=None, *args, **kwargs):
        self.ax = ax
        self.fig = fig
        self.world_recall = 0
        self.iterf = self.iter_frame()
        self._world_recall_reuslt_dict = world_recall_reuslt_dict
        if 'scmlworld' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['scmlworld'] = 'None'
        if 'current_step' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['current_step'] = -1
        if 'factories_managers' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['factories_managers'] = 'None'
        if 'consumers' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['consumers'] = 'None'
        if 'miners' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['miners'] = 'None'

    def iter_frame(self):
        step = 0
        step_information = 0
        while True:
            step_information = self._world_recall_reuslt_dict['current_step'] if 'current_step' in self._world_recall_reuslt_dict else 0
            scmlworld = self._world_recall_reuslt_dict['scmlworld']
            factories_managers = self._world_recall_reuslt_dict['factories_managers']
            consumers = self._world_recall_reuslt_dict['consumers']
            miners = self._world_recall_reuslt_dict['miners']
            yield [step_information, scmlworld, factories_managers, consumers, miners]
            step +=1

    def init(self):
        glovar.event.wait()
        step_information = self._world_recall_reuslt_dict['current_step'] if 'current_step' in self._world_recall_reuslt_dict else 0
        scmlworld = self._world_recall_reuslt_dict['scmlworld']
        factories_managers = self._world_recall_reuslt_dict['factories_managers']
        consumers = self._world_recall_reuslt_dict['consumers']
        miners = self._world_recall_reuslt_dict['miners']
        self.g = dnx.DynDiGraph(edge_removal=True)
        self.g.add_nodes_from(factories_managers)
        self.g.add_nodes_from(consumers)
        self.g.add_nodes_from(miners)
        self.pos =dnx.spring_layout(self.g,k=30,iterations=8)

        dnx.draw_networkx_nodes(self.g, pos=self.pos, with_labels=True)
        dnx.draw_networkx_labels(self.g,pos=self.pos,font_size=10)


    def update(self,frame):
        print('frame:' ,frame)
        interactions = itertools.combinations(self._world_recall_reuslt_dict['factories_managers'], 2)
        print(interactions)
        self.g.add_interactions_from(interactions, t=frame[0])
        # scat = self.ax.scatter(frame[0], frame[0])
        # self._world_recall_reuslt_dict['factories_managers']:
        #     self.g.add_interaction(u=frame[2][1], v=frame[3][1], t=frame[0])
        dnx.draw_networkx_edges(self.g, pos=self.pos, arrows=True)
        print('update a step')
        # return scat,

    def show(self):
        ai = FuncAnimation(self.fig, self.update, frames=self.iterf, interval=1000, init_func=self.init)
        plt.show(block = True)

if __name__ == "__main__":
    fig, ax = plt.subplots()
    world_recall_reuslt_dict = {'current_step':5, 'scmlworld':'test_world', 'factories_managers':['_df_1','my@1_2','greedy@2_2'],
                                                                'consumers':['c_0','c_1','c_2'], 'miners':['m_1', 'm_2', 'm_3']}
    a = ShowProcess(ax=ax, fig=fig, world_recall_reuslt_dict=world_recall_reuslt_dict)
    a.show()
import glovar
import sys
sys.path.append('../')
import dynetx as dnx
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# from threading import Event
import itertools
import negmas_draw
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

        node_name = [miners, factories_managers, consumers]
        layer_sizes = [len(layer) for layer in node_name]
        self.g = nx.DiGraph()
        self.g = negmas_draw.negmas_add_nodes(self.g, layer_sizes, node_name)
        self.pos = negmas_draw.negmas_layout(self.g, layer_sizes)
        negmas_draw.negmas_draw(self.g, negmas_draw.negmas_edge_colors, node_colors=negmas_draw.negmas_node_colors, pos=self.pos)


    def update(self,frame):
        print('frame:' ,frame)
        interactions = itertools.product(self._world_recall_reuslt_dict['miners'], self._world_recall_reuslt_dict['factories_managers'])
        self.g.add_edges_from(interactions)
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
import json
import os
from dataclasses import dataclass

from pyecharts import options as opts
from pyecharts.charts import Graph, Page, Liquid
from pyecharts.charts import Geo
from pyecharts.commons.types import Numeric, Optional, Sequence, Union
from pyecharts.globals import ChartType, SymbolType

from flask.json import jsonify
from flask import Flask, render_template
from app import FlaskAppWrapper
from networkx import DiGraph 
import sys
sys.path.append('../')
import negmas_draw

"""
mode:   'online_memory':  receive the data when run the simulator and at the same time update the graph (memory mode)
        'online_file'  :  save the world information of simulator at the running time into json file, and read data from 
                            file and update the graph 
        'offline'      :  read data from log file(json) at the end of simulator, with the time series, dynamic update the 
                            graph
        'debug'        : debug mode
"""

mode = 'debug'

@dataclass
class Setup_Graph:
    name: str
    linestyleopts: Union[Sequence[Union[opts.LineStyleOpts, dict]], None]
    categories: Union[Sequence[Union[opts.GraphCategory, dict]], None]
    graph: Union[DiGraph, dict]
    layer_sizes: list
    node_name: list

class DrawPyechart(object):
    def __init__(self, g: Union[DiGraph, None] = None, 
                    node_name=None, name=__name__, 
                    static_folder="templates", 
                    mode='online_memory'
        ):
        if g is not None:
            import sys
            sys.path.append('../')
            from negmas_draw import negmas_node_colors
            self.node_name = node_name
            self.layer_sizes = self._get_layer_sizes()
            g = negmas_draw.negmas_add_nodes(g, self.layer_sizes, self.node_name)
            self.g = g
        self._init()
        self.config = Setup_Graph(name, self.linestyleopts, self.categories, self.g, self.layer_sizes, self.node_name)
        self.a = FlaskAppWrapper(name, static_folder=static_folder)
        self.a.add_endpoint(rule='/', endpoint='home', view_func=self.index)
        self.a.add_endpoint(rule='/GraphChart', endpoint='GraphChart', view_func=self._graph_with_opts)
        self.a.add_endpoint(rule='/GraphDynamicData', endpoint='GraphDynamicData', view_func=self._graph_with_opts_dyn)
        self.a.run()
    
    def _init(self):
        self.linestyleopts = [
            opts.LineStyleOpts(width=5),
        ]
        try:
            categories ={self.g.nodes[node]['color'] for node in self.g.nodes}
            self.categories = [opts.GraphCategory(name='level_'+str(category)) for category in categories]
        except:
            self.categories = [
                opts.GraphCategory(name='c1'),
                opts.GraphCategory(name='c2'),
                opts.GraphCategory(name='c3'),
                opts.GraphCategory(name='c4'),
                opts.GraphCategory(name='c5'),
            ]
            print('default categories')


    def index(self):
        liquid = self._get_liquid_chart()
        return render_template("index.html", myechart=liquid.render_embed())
    
    @staticmethod
    def _get_liquid_chart():
        return liquid_base()
    
    def _get_layer_sizes(self):
        return [len(node) for node in self.node_name]
    
    def _graph_with_opts(self):
        nodes = [opts.GraphNode(name=node, 
                    x=self.config.graph.nodes[node]['pos'][0], 
                    y=self.config.graph.nodes[node]['pos'][1], 
                    symbol_size=10, category='level_'+str(self.config.graph.nodes[node]['color']))
                    for node in self.config.graph.nodes]
        links = []
        c = (
            Graph()
            .add("", nodes, links, self.categories, edge_symbol=['', 'arrow'], edge_symbol_size=10,layout='none', repulsion=4000,
            emphasis_itemstyle_opts=self.config.linestyleopts[0])
            .set_global_opts(title_opts=opts.TitleOpts(title="Graph-Negmas-Contract-Signed"))
        )
        return c.dump_options()
    
    def _graph_with_opts_dyn(self):
        g = negmas_draw.negmas_add_edges(self.config.graph, self.config.layer_sizes, node_name=self.config.node_name)
        edges = [(edge[0], edge[1]) for edge in g.edges]
        links = [opts.GraphLink(source=edge[0], target=edge[1]) for edge in edges]
        print(links[0].opts)
        result = []
        for link in links:
            result.append({"source": link.opts['source'], "target": link.opts['target']})
        return jsonify(result)

def get_layer_sizes(nodes):
    return [len(node) for node in nodes]

def index():
    # liquid = graph_with_opts()
    # return render_template("index.html", myechart=liquid.render_embed())
    return 'hello'

def draw_with_pyecharts():
    """
     use pyecharts to generate the echarts graph, and show the interactive graph with flask
     `pip install flask pyecharts networkx`
    """
    app = Flask(__name__, static_folder="templates")

def geo_base() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china")
        .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),
        )
    )
    return c

def geo_visualmap_piecewise() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="europe")
        # .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title="Geo-VisualMap（分段型）"),
        )
    )
    return c

def graph_with_opts_dyn() -> Sequence[Union[opts.GraphLink, dict]]:
    
    links = [
        opts.GraphLink(source="n2", target="n4"),
    ]
    return links

def graph_with_opts() -> Graph:
    g = []
    layer_sizes = [2, 2, 1]
    pos = negmas_draw.negmas_layout(g, layer_sizes)
    nodes = [
        opts.GraphNode(name="n1", x=pos[0][0], y=pos[0][1], symbol_size=10, category='c1'),
        opts.GraphNode(name="n2", x=pos[1][0], y=pos[1][1], symbol_size=20, category='c2'),
        opts.GraphNode(name="n3", x=pos[2][0], y=pos[2][1], symbol_size=30, category='c3'),
        opts.GraphNode(name="n4", x=pos[3][0], y=pos[3][1], symbol_size=40, category='c1'),
        opts.GraphNode(name="n5", x=pos[4][0], y=pos[4][1], symbol_size=50, category='c1'),
    ]
    
    linestyleopts = [
        opts.LineStyleOpts(width=5),
        ]
    
    links = [
        opts.GraphLink(source="n1", target="n2"),
        opts.GraphLink(source="n2", target="n3"),
        opts.GraphLink(source="n3", target="n4"),
        opts.GraphLink(source="n4", target="n5"),
        opts.GraphLink(source="n5", target="n1"),
    ]

    categories = [
        opts.GraphCategory(name='c1'),
        opts.GraphCategory(name='c2'),
        opts.GraphCategory(name='c3'),
        opts.GraphCategory(name='c4'),
        opts.GraphCategory(name='c5'),
        ]
    
    c = (
        Graph()
        .add("", nodes, links, categories, edge_symbol=['', 'arrow'], edge_symbol_size=10,layout='none', repulsion=4000,
        emphasis_itemstyle_opts=linestyleopts[0])
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink"))
    )
    return c

def liquid_base() -> Liquid:
    c = (
        Liquid()
        .add("lq", [0.6, 0.7])
        .set_global_opts(title_opts=opts.TitleOpts(title="Process"))
    )
    return c

# graph_with_opts().render('k.html')
if __name__ == '__main__':
    g = DiGraph()
    nodes = [['m_1', 'm_2', 'm_3'], ['f_1', 'f_2'], ['g_1', 'g_2'], ['c_1', 'c_2']]
    DrawPyechart(g=g, node_name=nodes, name='DrawPyecharts')
from random import randrange

from flask.json import jsonify
from flask import Flask, render_template, Response

from pyecharts import options as opts
from pyecharts.charts import Line
# from ech import liquid_base, graph_with_opts

app = Flask(__name__, static_folder="templates")

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name=__name__, static_folder="templates"):
        self.app = Flask(name, static_folder=static_folder)
    
    def run(self):
        return self.app.run()
    
    def add_endpoint(self, rule, endpoint=None, view_func=None, handler=None):
        self.app.add_url_rule(rule, endpoint=endpoint, view_func=view_func)


def line_base() -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(i) for i in range(10)])
        .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@app.route("/")
def index():
    liquid = get_liquid_chart()
    return render_template("index.html", myechart=liquid.render_embed())


@app.route("/GraphChart")
def get_graph_chart():
    c = graph_with_opts()
    return c.dump_options()


idx = 9


@app.route("/lineDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": randrange(50, 80)})

@app.route("/liquid")
def get_liquid_chart():
    c = liquid_base()
    return c

if __name__ == "__main__":
    app.run()
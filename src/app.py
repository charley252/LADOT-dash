import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px



app = Dash(__name__)
server = app.server



app.layout = html.Div(children=[html.H1(children='Hello World')])




# @callback(
#     Output(),
#     Input()
# )
# def update_graph(value):
#     return value






if __name__=='__main__':
    app.run(debug=True)




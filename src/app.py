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






if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))




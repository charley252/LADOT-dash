# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Incorporate data
# df = pd.read_csv('src/gps1_elev.txt', sep='\t')
df = pd.read_csv('src/august_threeToseven_i_d_export.csv')

fig = px.scatter_map(df, lat="latitude", lon="longitude", zoom=11, height=300)
fig.update_layout(map_style="dark")
fig.update_layout(margin={"r":500,"t":0,"l":500,"b":0})
fig.update_geos(fitbounds='locations')
# fig.show()


# Initialize the app
app = Dash()

# App layout
app.layout = dcc.Graph(figure=fig)


# Add controls to build the interaction
# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=True)

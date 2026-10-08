import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px


app = Dash(__name__)
server = app.server


#df = pd.read_csv('src/august_threeToseven_i_d_export.csv', index_col=0, parse_dates=True)
df = pd.read_csv('august_threeToseven_i_d_export.csv', index_col=0, parse_dates=True)
df_r = df.reset_index()  # moves index into a column


#app.layout = html.Div("Dashboard coming soon!")
app.layout = html.Div([dash_table.DataTable(
        data=df_r.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_r.columns],
        page_size=10),
        
        html.Div(dcc.Dropdown(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ['Monday'], id='days', multi=True)),

        html.Div([dcc.Graph(id='map'),
            dcc.Graph(id="power"),
            dcc.Graph(id="current"),
            dcc.Graph(id="voltage"),
            dcc.Graph(id="grade"),
            dcc.Graph(id="acceleration"),
            dcc.Graph(id="speed"),
            dcc.Graph(id="elevation")])
        ])



@callback(
    Output('power', 'figure'),
    Output('current', 'figure'),
    Output('voltage', 'figure'),
    Output('grade', 'figure'),
    Output('acceleration', 'figure'),
    Output('speed', 'figure'),
    Output('elevation', 'figure'),
    Output('map', 'figure'),
    Input('days', 'value')
)
def update_figure(selected_day):
#     august_threeToseven_i_d_export[august_threeToseven_i_d_export['DayofWeek'] =='Monday']
    selectedDay_df = df_r[df_r['DayofWeek'].isin(selected_day)]

    fig1 = px.line(selectedDay_df, x="DateTime", y="Power", color='DayofWeek', template='plotly_dark')
    fig2 = px.line(selectedDay_df, x="DateTime", y="Current", color='DayofWeek', template='plotly_dark')
    fig3 = px.line(selectedDay_df, x="DateTime", y="Voltage", color='DayofWeek', template='plotly_dark')
    fig4 = px.line(selectedDay_df, x="DateTime", y="Grade", color='DayofWeek', template='plotly_dark')
    fig5 = px.line(selectedDay_df, x="DateTime", y="Acceleration", color='DayofWeek', template='plotly_dark')
    fig6 = px.line(selectedDay_df, x="DateTime", y="Speed", color='DayofWeek', template='plotly_dark')
    fig7 = px.line(selectedDay_df, x="DateTime", y="Elevation", color='DayofWeek', template='plotly_dark')

    fig1.update_layout(transition_duration=500)
    fig2.update_layout(transition_duration=500)
    fig3.update_layout(transition_duration=500)
    fig4.update_layout(transition_duration=500)
    fig5.update_layout(transition_duration=500)
    fig6.update_layout(transition_duration=500)
    fig7.update_layout(transition_duration=500)

    map = px.scatter_map(selectedDay_df, lat="latitude", lon="longitude", color='DayofWeek', zoom=11, height=300)
    map.update_layout(map_style="dark")
    map.update_layout(margin={"r":500,"t":0,"l":500,"b":0})
    map.update_geos(fitbounds='locations')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, map



if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8050))) # app.run_server has been deprecated.
    app.run(debug=True)




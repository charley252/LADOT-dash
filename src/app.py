import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px



#df = pd.read_csv('src/august_threeToseven_i_d_export.csv', index_col=0, parse_dates=True)
df = pd.read_csv('august_threeToseven_i_d_export.csv', index_col=0, parse_dates=True)
df_r = df.reset_index()  # moves index into a column

excluded_columns = ['Hour', '30Min', '1Min']

app = Dash(__name__)
server=app.server

app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "height": "100vh",
        "padding": "10px",
        #'backgroundColor': '#1e1e1e'
    },
    children=[
        # Title
        html.Div(
            "LADOT EV Bus Analysis",
            style={"fontSize": "30px", "fontWeight": "bold", "marginBottom": "10px"}
        ),

        # Dropdown
        html.Div(
            dcc.Dropdown(
                ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ['Monday'],
                id='days',
                multi=True,
                style={"width": "300px"}
            ),
            style={"marginBottom": "20px"}
        ),

        # Main layout
        html.Div(
            style={
                "display": "flex",
                "flex": "1",
                "width": "100%",
                "gap": "10px",
                "padding": "10px",
            },
            children=[
                # LEFT COLUMN (Table + Map)
                html.Div(
                    style={
                        "flex": "1",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "10px",
                        "minWidth": "400px",
                        #'backgroundColor': '#1e1e1e'
                    },
                    children=[
                        # Table with dash_table
                        dash_table.DataTable(
                            id='ladot-table',
                            # columns=[{"name": i, "id": i} for i in df_r.columns],
                            columns=[{"name": i, "id": i} for i in df_r.columns if i not in excluded_columns],
                            data=df_r.to_dict('records'),
                            fixed_rows={'headers': True},
                            style_table={
                                'height': '300px',
                                'overflowY': 'auto',
                                #'backgroundColor': '#1e1e1e'
                            },
    
                            style_cell={
                                'textAlign': 'left',
                                'fontSize': '12px',
                                'padding': '5px',
                                'whiteSpace': 'normal',     # Allow wrapping inside cells if needed
                                'height': 'auto',
                                'minWidth': '50px',          # << minimum width
                                'width': '100px',            # << preferred width
                                'maxWidth': '150px',         # << maximum width
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                # 'backgroundColor': '#1e1e1e',
                                # 'color': '#d3d3d3',
                                # 'border': '1px solid #333'
                            },
    
                            style_header={
                                'fontSize': '12px',      # << Slightly bigger font for headers (optional)
                                'fontWeight': 'bold',
                                'backgroundColor': 'lightgrey',
                                'textAlign': 'center',
                                # 'backgroundColor': '#333333',
                                # 'borderBottom': '2px solid #555',
                                # 'color': '#ffffff'
                            },
                        ),

                        # Map
                        dcc.Graph(
                            id='fig_map',
                            #figure=city_map,
                            style={"flex": "2"}
                        ),
                    ]
                ),

                # RIGHT COLUMN (Graphs stacked)
                html.Div(
                    style={
                        "flex": "1",
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "10px",
                        "minWidth": "300px",
                    },
                    children=[
                        html.Div(
                            style={
                                "flex": "1",
                                "display": "flex",
                                "flexDirection": "column",
                                "gap": "10px",
                            },
                            children=[
                                dcc.Graph(id="power", style={"flex": "1"}),
                                dcc.Graph(id="current", style={"flex": "1"}),
                                dcc.Graph(id="voltage", style={"flex": "1"}),
                                ]
                            ),

                        html.Div(
                            style={
                                "flex": "1",
                                "display": "flex",
                                "flexDirection": "column",
                                "gap": "10px",
                            },
                            children=[
                                dcc.Graph(id="grade", style={"flex": "1"}),
                                dcc.Graph(id="acceleration", style={"flex": "1"}),
                                dcc.Graph(id="speed", style={"flex": "1"}),
                                dcc.Graph(id="elevation", style={"flex": "1"})
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]
    )

@callback(
    Output('power', 'figure'),
    Output('current', 'figure'),
    Output('voltage', 'figure'),
    Output('grade', 'figure'),
    Output('acceleration', 'figure'),
    Output('speed', 'figure'),
    Output('elevation', 'figure'),
    Output('fig_map', 'figure'),
    Input('days', 'value')
)
def update_figure(selected_day):
    selectedDay_df = df_r[df_r['DayofWeek'].isin(selected_day)]

    fig1 = px.line(selectedDay_df, x="DateTime", y="Power", color='DayofWeek', template='seaborn')
    fig2 = px.line(selectedDay_df, x="DateTime", y="Current", color='DayofWeek', template='seaborn')
    fig3 = px.line(selectedDay_df, x="DateTime", y="Voltage", color='DayofWeek', template='seaborn')
    fig4 = px.line(selectedDay_df, x="DateTime", y="Grade", color='DayofWeek', template='seaborn')
    fig5 = px.line(selectedDay_df, x="DateTime", y="Acceleration", color='DayofWeek', template='seaborn')
    fig6 = px.line(selectedDay_df, x="DateTime", y="Speed", color='DayofWeek', template='seaborn')
    fig7 = px.line(selectedDay_df, x="DateTime", y="Elevation", color='DayofWeek', template='seaborn')

    fig1.update_layout(transition_duration=500)
    fig2.update_layout(transition_duration=500)
    fig3.update_layout(transition_duration=500)
    fig4.update_layout(transition_duration=500)
    fig5.update_layout(transition_duration=500)
    fig6.update_layout(transition_duration=500)
    fig7.update_layout(transition_duration=500)

    map_center_df = selectedDay_df if not selectedDay_df.empty else df_r
    fig_map = px.scatter_map(
        selectedDay_df,
        lat="latitude",
        lon="longitude",
        color='DayofWeek',
        center={
            "lat": map_center_df["latitude"].mean(),
            "lon": map_center_df["longitude"].mean(),
        },
        zoom=11,
        height=300,
    )
    fig_map.update_layout(map_style="carto-positron")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_geos(fitbounds='locations')


    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig_map

if __name__ == '__main__':
    app.run(debug=True)

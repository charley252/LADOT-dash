# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Example data
df = pd.DataFrame({
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Population": [8419600, 3980400, 2716000, 2328000, 1690000]
})

# Dash app
app = Dash(__name__)

app.layout = html.Div(
    style={
        "display": "flex",
        "height": "100vh",
        "padding": "10px",
        "gap": "10px"
    },
    children=[
        # Middle section: Table on top, Map below
        html.Div(
            style={
                "flex": "2",
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px"
            },
            children=[
                # Table
                html.Div(
                    style={
                        "flex": "1",
                        "border": "1px solid #ccc",
                        "padding": "10px",
                        "overflow": "auto"
                    },
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'),
                            style_table={"height": "100%", "overflowY": "auto"},
                        )
                    ]
                ),
                # Map
                html.Div(
                    style={
                        "flex": "2",
                        "border": "1px solid #ccc",
                        "padding": "10px",
                    },
                    children=[
                        dcc.Graph(
                            figure=px.scatter_mapbox(
                                df,
                                lat=[40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
                                lon=[-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
                                hover_name="City",
                                size="Population",
                                zoom=3
                            ).update_layout(mapbox_style="open-street-map")
                        )
                    ]
                ),
            ]
        ),
        # Right side: 4 stacked graphs
        html.Div(
            style={
                "flex": "1",
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px"
            },
            children=[
                html.Div(
                    style={"flex": "1", "border": "1px solid #ccc", "padding": "5px"},
                    children=[dcc.Graph(figure=px.line(df, x="City", y="Population"))]
                ),
                html.Div(
                    style={"flex": "1", "border": "1px solid #ccc", "padding": "5px"},
                    children=[dcc.Graph(figure=px.bar(df, x="City", y="Population"))]
                ),
                html.Div(
                    style={"flex": "1", "border": "1px solid #ccc", "padding": "5px"},
                    children=[dcc.Graph(figure=px.scatter(df, x="City", y="Population"))]
                ),
                html.Div(
                    style={"flex": "1", "border": "1px solid #ccc", "padding": "5px"},
                    children=[dcc.Graph(figure=px.area(df, x="City", y="Population"))]
                ),
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

# Initialize the app
app = Dash(__name__)

# City population dataset
df = pd.DataFrame({
    "City": ["San Francisco", "Los Angeles", "New York", "Chicago"],
    "Population": [883305, 3990456, 8175133, 2714856],
    "Latitude": [37.7749, 34.0522, 40.7128, 41.8781],
    "Longitude": [-122.4194, -118.2437, -74.0060, -87.6298]
})

# Create a bar plot of the populations
population_bar = px.bar(df, x="City", y="Population", title="City Populations")

# Create a map plot using the latitude and longitude
city_map = px.scatter_geo(df, lat="Latitude", lon="Longitude", hover_name="City", size="Population",
                          projection="natural earth", title="Cities Map")

# Create a scatter plot for city populations over time (dummy example)
city_scatter = px.scatter(df, x="City", y="Population", color="City", title="City Population Scatter")

# Create a line plot for population growth (dummy example)
city_line = px.line(df, x="City", y="Population", title="City Population Growth (Line Plot)")

# Create a histogram of the population distribution
city_histogram = px.histogram(df, x="Population", nbins=20, title="Population Distribution Histogram")

# Create the layout with 4 sections: Title, Dropdown, Table (left) and Graphs (right)
app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",  # Layout in column mode to stack the title and dropdown
        "alignItems": "center",
        "height": "100vh",
        "gap": "10px",
        "padding": "10px",
    },
    children=[
        # Title Section
        html.Div(
            style={
                "fontSize": "30px",
                "fontWeight": "bold",
                "marginBottom": "10px",
            },
            children="City Population Dashboard"
        ),
        
        # Dropdown Section
        html.Div(
            style={
                "marginBottom": "20px",  # Space between dropdown and other content
            },
            children=[
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[
                        {'label': city, 'value': city} for city in df['City']
                    ],
                    value='San Francisco',  # Default value
                    style={"width": "300px"}
                ),
            ]
        ),

        # Main Content Section (Table and Graphs)
        html.Div(
            style={
                "display": "flex",
                "flex": "1",
                "flexWrap": "wrap",        # Allow wrapping on smaller screens
                "gap": "10px",
                "width": "100%",
                "padding": "10px",
            },
            children=[
                # LEFT: Table and Map stacked (taking 2/3 of the space)
                html.Div(
                    style={
                        "flex": "2",  # This makes it take 2/3 of the space
                        "minWidth": "400px",  # Prevent it from shrinking too much
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "10px",
                        "transition": "all 0.5s ease",
                    },
                    children=[
                        html.Div(
                            id='table-container',
                            style={
                                "flex": "1",
                                "border": "1px solid black",
                                "padding": "10px",
                                "transition": "all 0.5s ease",
                                "overflowY": "auto",   # Scroll if table too tall
                            },
                            children=[
                                # HTML Table to display the data
                                html.Table(
                                    style={"width": "100%", "borderCollapse": "collapse"},
                                    children=[
                                        html.Tr([html.Th("City"), html.Th("Population"), html.Th("Latitude"), html.Th("Longitude")]),
                                        *[
                                            html.Tr([html.Td(city), html.Td(pop), html.Td(lat), html.Td(lon)])
                                            for city, pop, lat, lon in zip(df["City"], df["Population"], df["Latitude"], df["Longitude"])
                                        ]
                                    ]
                                )
                            ]
                        ),
                        dcc.Graph(
                            id='map',
                            figure=city_map,
                            style={
                                "flex": "2",
                                "transition": "all 0.5s ease",
                            }
                        ),
                    ]
                ),

                # RIGHT: Column of 4 graphs stacked (taking 1/3 of the space)
                html.Div(
                    style={
                        "flex": "1",  # This makes it take 1/3 of the space
                        "minWidth": "300px",  # Prevent squashing
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "10px",
                        "transition": "all 0.5s ease",
                    },
                    children=[
                        dcc.Graph(id='population-bar', figure=population_bar, style={"flex": "1", "transition": "all 0.5s ease"}),
                        dcc.Graph(id='city-scatter', figure=city_scatter, style={"flex": "1", "transition": "all 0.5s ease"}),
                        dcc.Graph(id='city-line', figure=city_line, style={"flex": "1", "transition": "all 0.5s ease"}),
                        dcc.Graph(id='city-histogram', figure=city_histogram, style={"flex": "1", "transition": "all 0.5s ease"}),
                    ]
                ),
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run(debug=True)

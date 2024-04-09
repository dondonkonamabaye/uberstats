#import pygal.maps.world

import time
from tracemalloc import start

import numpy as np

from pandas import Series, DataFrame

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1

import mplleaflet
from IPython.display import IFrame

import base64
from PIL import Image
import io

import hvplot.pandas

import requests # Pour effectuer la requête
import pandas as pd # Pour manipuler les données
import datetime as dt

import param
import panel as pn

import plotly.express as px

import mysql.connector

import dash
#from sklearn.datasets import load_wine
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries

from dash.dash_table import DataTable


#########################################################################################################################################################################

df = pd.read_csv("My Uber Drives - 2016.csv")

df.dropna(inplace=True)

# convert the timestamp column to datetime format
df['START_DATE*'] = pd.to_datetime(df['START_DATE*'])
df['END_DATE*'] = pd.to_datetime(df['END_DATE*'])

# calculate the time difference between consecutive rows
df['Diff in Days'] = df['END_DATE*'] - df['START_DATE*']
df['Diff in Seconds'] = (df['END_DATE*'] - df['START_DATE*']).dt.total_seconds()
df['Diff in Minutes'] = (df['END_DATE*'] - df['START_DATE*']).dt.total_seconds() / 60
df['Diff in Hours'] = (df['END_DATE*'] - df['START_DATE*']).dt.total_seconds() / 60 / 60

# filter in months
df['START MONTH'] = df['START_DATE*'].dt.month
df['END MONTH'] = df['END_DATE*'].dt.month

# df['START MONTH'] = df['START MONTH'].strftime("%B")
# df['END MONTH']   = df['END MONTH'].strftime("%B")

# list_month_name = []

# for month_name in df['START MONTH']:
#     list_month_name.append(month_name.strftime("%B"))

#########################################################################################################################################################################

max_diff_minutes = df['Diff in Minutes'].max()
df_max_minutes = df[(df['Diff in Minutes'] == max_diff_minutes)]

start_max_minutes = df_max_minutes['START*'].values
stop_max_minutes = df_max_minutes['STOP*'].values
max_distance_miles = df_max_minutes['MILES*'].values
max_purpose_values = df_max_minutes['PURPOSE*'].values

min_diff_minutes = df['Diff in Minutes'].min()
df_min_minutes = df[(df['Diff in Minutes'] == min_diff_minutes)]
min_distance_miles = df_min_minutes['MILES*'].values
min_purpose_values = df_min_minutes['PURPOSE*'].values

start_min_minutes = df_min_minutes['START*'].values
stop_min_minutes = df_min_minutes['STOP*'].values

message_max = f"The visit purpose of {max_purpose_values[0]} is the highest time in minutes between {start_max_minutes[0]} and {stop_max_minutes[0]} is {max_diff_minutes} min for a distance of {max_distance_miles[0]} miles."
message_min = f"The visit purpose of {min_purpose_values[0]} is the lowest time in minutes between {start_min_minutes[0]} and {stop_min_minutes[0]} is {min_diff_minutes} min for a distance of {min_distance_miles[0]} miles."

#########################################################################################################################################################################

max_miles = df['MILES*'].max()
df_max_miles = df[(df['MILES*'] == max_miles)]

start_max_miles = df_max_miles['START*'].values
stop_max_miles = df_max_miles['STOP*'].values
max_distance_miles = df_max_miles['MILES*'].values
max_purpose_values = df_max_miles['PURPOSE*'].values

min_miles = df['MILES*'].min()
df_min_miles = df[(df['MILES*'] == min_miles)]
min_distance_miles = df_min_miles['MILES*'].values
min_purpose_values = df_min_miles['PURPOSE*'].values

start_min_miles = df_min_miles['START*'].values
stop_min_miles = df_min_miles['STOP*'].values

message_miles_max = f"The visit purpose of {max_purpose_values[0]} is the highest time in minutes between {start_max_miles[0]} and {stop_max_miles[0]} is {max_miles} miles for a distance of {max_distance_miles[0]} miles."
message_miles_min = f"The visit purpose of {min_purpose_values[0]} is the lowest time in minutes between {start_min_miles[0]} and {stop_min_miles[0]} is {min_miles} miles for a distance of {min_distance_miles[0]} miles."

##############################################################################################################################################################################################################################

values_unique_category = df['CATEGORY*'].unique()

numeric_values_miles = ['MILES*']
values_unique_dates = ['Diff in Minutes']
color_start = df['CATEGORY*']

# values_unique_dates = ['Diff in Seconds', 'Diff in Minutes', 'Diff in Hours']

def create_category_bar(values_unique_category='Business', values_unique_dates = 'Diff in Minutes'):
    filtered_df_category = df[(df['CATEGORY*'] == values_unique_category)]
    filtered_df_category = filtered_df_category.sort_values(by='MILES*', ascending=False)

    bar_fig = px.bar(filtered_df_category, x="PURPOSE*", y=values_unique_dates, hover_name="PURPOSE*",
    barmode="relative", hover_data="PURPOSE*", custom_data="PURPOSE*", template="seaborn", 
    title=f"{values_unique_category} & {values_unique_dates}", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6',  height=450)
    
    return bar_fig

multi_select_category_bar = dcc.Dropdown(id='multi_select_category_bar', options=values_unique_category, value='Business', clearable=False)
multi_select_dates_bar = dcc.Dropdown(id='multi_select_dates_bar', options=values_unique_dates, value='Diff in Minutes', clearable=False)


#########################################################################################################################################################################

values_unique_category = df['CATEGORY*'].unique()

numeric_values_miles = ['MILES*']
values_unique_dates = ['Diff in Minutes']


def create_category_pie(values_unique_category='Business', values_unique_dates = 'Diff in Minutes'):
    filtered_df_category =  df[(df['CATEGORY*'] == values_unique_category)]
    filtered_df_category = filtered_df_category.sort_values(by='MILES*', ascending=False)

    pie_fig = px.pie(filtered_df_category, values=values_unique_dates, names="PURPOSE*", template="seaborn",
    hover_data="PURPOSE*", custom_data="PURPOSE*", title=f"{values_unique_category} & {values_unique_dates}")
    pie_fig.update_layout(paper_bgcolor='#e5ecf6', height=450)

    return pie_fig

multi_select_category_pie = dcc.Dropdown(id='multi_select_category_pie', options=values_unique_category, value='Business', clearable=False)
multi_select_dates_pie = dcc.Dropdown(id='multi_select_dates_pie', options=values_unique_dates, value='Diff in Minutes', clearable=False)

#########################################################################################################################################################################

values_unique_category = df['CATEGORY*'].unique()
values_unique_purposes = df['PURPOSE*'].unique()
values_unique_start_end = ['START*', 'END*']
values_unique_start = df['PURPOSE*'].unique()
values_unique_stop = df['PURPOSE*'].unique()

numeric_values_miles = ['MILES*']
values_unique_dates = ['Diff in Minutes']

def create_category_scatter_start(values_unique_category='Business', values_unique_stop='Meeting'):
    filtered_df_category_scatter = df[(df['CATEGORY*'] == values_unique_category) & (df['PURPOSE*'] == values_unique_stop)]
    filtered_df_category_scatter = filtered_df_category_scatter.sort_values(by='MILES*', ascending=False)

    scatter_fig = px.scatter(filtered_df_category_scatter, x="MILES*", y='START*', title=f"Category {values_unique_category} vs Purposes {values_unique_stop}")
    scatter_fig.update_layout(height=450)
    return scatter_fig
    

multi_select_category_scatter_start = dcc.Dropdown(id='multi_select_category_scatter_start', options=values_unique_category, value='Business', clearable=False)
multi_select_scatter_stop = dcc.Dropdown(id='multi_select_scatter_stop', options=values_unique_stop, value='Meeting', clearable=False)
#multi_select_start_end_scatter = dcc.Dropdown(id='multi_select_start_end_scatter', options=values_unique_start_end, value='START*', clearable=False)


#########################################################################################################################################################################

values_unique_category = df['CATEGORY*'].unique()
values_unique_purposes = df['PURPOSE*'].unique()
values_unique_start_end = ['START*', 'END*']

numeric_values_miles = ['MILES*']
values_unique_dates = ['Diff in Minutes']

def create_category_scatter_stop(values_unique_category='Business', values_unique_start='Meeting'):
    filtered_df_category_scatter = df[(df['CATEGORY*'] == values_unique_category) & (df['PURPOSE*'] == values_unique_start)]
    filtered_df_category_scatter = filtered_df_category_scatter.sort_values(by='MILES*', ascending=False)

    scatter_fig = px.scatter(filtered_df_category_scatter, x="MILES*", y='STOP*', title=f"Category {values_unique_category} vs Purposes {values_unique_start}")
    scatter_fig.update_layout(height=450)
    return scatter_fig
    

multi_select_category_scatter_stop = dcc.Dropdown(id='multi_select_category_scatter_stop', options=values_unique_category, value='Business', clearable=False)
multi_select_scatter_start = dcc.Dropdown(id='multi_select_scatter_start', options=values_unique_start, value='Meeting', clearable=False)
#multi_select_start_end_scatter = dcc.Dropdown(id='multi_select_start_end_scatter', options=values_unique_start_end, value='START*', clearable=False)


#########################################################################################################################################################################


values_unique_category = df['CATEGORY*'].unique()
values_unique_purposes = df['PURPOSE*'].unique()
values_unique_start_end = ['START*', 'END*']
values_unique_stop = df['STOP*']

numeric_values_miles = ['MILES*']
values_unique_miles = df['MILES*']
values_unique_dates = ['Diff in Minutes']


def create_category_density_heatmap_start(values_unique_category='Business', values_unique_purposes='Meeting'):
    filtered_df = df[(df['CATEGORY*'] == values_unique_category) & (df['PURPOSE*'] == values_unique_purposes)]
    filtered_df = filtered_df.sort_values(by="MILES*", ascending=False).head(50)

    bar_fig = px.density_heatmap(filtered_df, x="MILES*", y="START*" , z="Diff in Hours", template="seaborn",
    color_continuous_scale="Viridis", title=f"Category {values_unique_category} vs Purposes {values_unique_purposes}", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=540)
    
    return bar_fig


multi_select_category_density_heatmap_start = dcc.Dropdown(id='multi_select_category_density_heatmap_start', options=values_unique_category, value='Business', clearable=False)
multi_select_density_heatmap_start = dcc.Dropdown(id='multi_select_density_heatmap_start', options=values_unique_start, value='Meeting', clearable=False)
multi_select_density_heatmap_purposes_start = dcc.Dropdown(id='multi_select_density_heatmap_purposes_start', options=values_unique_purposes, value='Meeting', clearable=False)

#########################################################################################################################################################################



values_unique_category = df['CATEGORY*'].unique()
values_unique_purposes = df['PURPOSE*'].unique()
values_unique_start_end = ['START*', 'END*']
values_unique_stop = df['STOP*']

numeric_values_miles = ['MILES*']
values_unique_miles = df['MILES*']
values_unique_dates = ['Diff in Minutes']


def create_category_density_heatmap_stop(values_unique_category='Business', values_unique_purposes='Meeting'):
    filtered_df = df[(df['CATEGORY*'] == values_unique_category) & (df['PURPOSE*'] == values_unique_purposes)]
    filtered_df = filtered_df.sort_values(by="MILES*", ascending=False).head(50)

    bar_fig = px.density_heatmap(filtered_df, x="MILES*", y="STOP*" , z="Diff in Hours", template="seaborn",
    color_continuous_scale="Viridis", title=f"Category {values_unique_category} vs Purposes {values_unique_purposes}", text_auto=True)
    bar_fig.update_layout(paper_bgcolor='#e5ecf6', height=540)
    
    return bar_fig


multi_select_category_density_heatmap_stop = dcc.Dropdown(id='multi_select_category_density_heatmap_stop', options=values_unique_category, value='Business', clearable=False)
multi_select_density_heatmap_stop = dcc.Dropdown(id='multi_select_density_heatmap_stop', options=values_unique_start, value='Meeting', clearable=False)
multi_select_density_heatmap_purposes_stop = dcc.Dropdown(id='multi_select_density_heatmap_purposes_stop', options=values_unique_purposes, value='Meeting', clearable=False)

#########################################################################################################################################################################

minutes_sum = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['Diff in Minutes'].sum(),
        title={'text':'Total Diff  Minutes'},
    )
)
minutes_sum.update_layout(title="", height=250)

minutes_max = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['Diff in Minutes'].max(),
        title={'text':'Maximum Diff Minutes'},
    )
)
minutes_max.update_layout(title="", height=250)

minutes_min = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['Diff in Minutes'].min(),
        title={'text':'Minimum Diff Minutes'},
    )
)
minutes_min.update_layout(title="", height=250)

#########################################################################################################################################################################


miles_sum = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['MILES*'].sum(),
        title={'text':'Total Miles'},
    )
)
miles_sum.update_layout(title="", height=250)

miles_max = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['MILES*'].max(),
        title={'text':'Maximum Miles'},
    )
)
miles_max.update_layout(title="", height=250)

miles_min = go.FigureWidget(
    go.Indicator(
        mode="number",
        value=df['MILES*'].min(),
        title={'text':'Minimum Miles'},
    )
)
miles_min.update_layout(title="", height=250)

#########################################################################################################################################################################


app = Dash(title="Uber Drive Dashboard Report")

app.layout = html.Div(
        children=[
            html.H1("Uber Drive Mobility Statistics", style={"text-align":"center"}),


            dcc.Tabs
            ([
            dcc.Tab(label="TOP UBER DRIVE MOBILITY STATISTICS",
                children=
                 [  
                    html.Div
                    ( 
                        children=
                        [
                            html.H3('This is the total, maximum and minimum miles in numbers differents between each trip.', style={"text-align":"center"}),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=miles_sum),
                                ],

                                style={"display": "inline-block", "width": "33%"} 
                            ),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=miles_max),
                                ],
            
                                style={"display": "inline-block", "width": "33%"} 
                            ),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=miles_min),
                                ],
                                style={"display": "inline-block", "width": "33%"} 
                            ),


                            multi_select_category_bar, multi_select_dates_bar,
                            dcc.Graph(id='category_bar', figure=create_category_bar()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),  

                    html.Div
                    ( 
                        children=
                        [
                            html.H3('This is the total, maximum and minimum times in minutes differents between each trip.', style={"text-align":"center"}),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=minutes_sum),
                                ],

                                style={"display": "inline-block", "width": "33%"} 
                            ),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=minutes_max),
                                ],
            
                                style={"display": "inline-block", "width": "33%"} 
                            ),

                            html.Div
                            ( 
                                children=
                                [
                                    dcc.Graph(figure=minutes_min),
                                ],
                                style={"display": "inline-block", "width": "33%"} 
                            ),


                            multi_select_category_pie, multi_select_dates_pie,
                            dcc.Graph(id='category_pie', figure=create_category_pie()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),  

                    html.Br(),
                    html.Br(),
                    
                    html.Div
                    ( 
                        children=
                        [
                            multi_select_category_scatter_start, multi_select_scatter_stop,
                            dcc.Graph(id='category_scatter_start', figure=create_category_scatter_start()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_category_scatter_stop, multi_select_scatter_start,
                            dcc.Graph(id='category_scatter_stop', figure=create_category_scatter_stop()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_category_density_heatmap_start, multi_select_density_heatmap_purposes_start,
                            dcc.Graph(id='category_density_heatmap_start', figure=create_category_density_heatmap_start()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),

                    html.Div
                    ( 
                        children=
                        [
                            multi_select_category_density_heatmap_stop, multi_select_density_heatmap_purposes_stop,
                            dcc.Graph(id='category_density_heatmap_stop', figure=create_category_density_heatmap_stop()),
                        ],
                        style={"display": "inline-block", "width": "50%"} 
                    ),
                ],
            ),
        ]),
    ],
    style={"padding":"50px"}
)


@callback(Output('category_bar', "figure"), [Input('multi_select_category_bar', "value"), ], [Input('multi_select_dates_bar', "value"), ],)
def update_category_bar(values_unique_category, values_unique_dates):
    return create_category_bar(values_unique_category, values_unique_dates)


@callback(Output('category_pie', "figure"), [Input('multi_select_category_pie', "value"), ], [Input('multi_select_dates_pie', "value"), ],)
def update_category_pie(values_unique_category, values_unique_dates):
    return create_category_pie(values_unique_category, values_unique_dates)


@callback(Output('category_scatter_start', "figure"), [Input('multi_select_category_scatter_start', "value"), ], [Input('multi_select_scatter_stop', "value"), ],)
def update_category_scatter_start(values_unique_category, values_unique_stop):
    return create_category_scatter_start(values_unique_category, values_unique_stop)


@callback(Output('category_scatter_stop', "figure"), [Input('multi_select_category_scatter_stop', "value"), ], [Input('multi_select_scatter_start', "value"), ],)
def update_category_scatter_stop(values_unique_category, values_unique_start):
    return create_category_scatter_stop(values_unique_category, values_unique_start)


@callback(Output('category_density_heatmap_start', "figure"), [Input('multi_select_category_density_heatmap_start', "value"), ], [Input('multi_select_density_heatmap_purposes_start', "value"), ],)
def update_category_density_heatmap_start(values_unique_category, values_unique_purposes):
    return create_category_density_heatmap_start(values_unique_category, values_unique_purposes)


@callback(Output('category_density_heatmap_stop', "figure"), [Input('multi_select_category_density_heatmap_stop', "value"), ], [Input('multi_select_density_heatmap_purposes_stop', "value"), ],)
def update_category_density_heatmap_stop(values_unique_category, values_unique_purposes):
    return create_category_density_heatmap_stop(values_unique_category, values_unique_purposes)

if __name__ == "__main__":
    app.run_server(debug=True)
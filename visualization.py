import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import datetime

from utils import utils
u = utils()


@st.cache_data(hash_funcs={dict: lambda _: None}, show_spinner="Generating Plot")
def scatter_map_anim(filtered_df):
    chart_dict = {}
    fig_map = px.scatter_mapbox(
        filtered_df.sort_values("event_date").dropna(),
        lat="latitude",
        lon="longitude", 
        animation_frame = "event_date",
        # range_color = (min(filtered_df["event_type"]), max(filtered_df["event_type"])),
        hover_name="event_id_cnty",
        hover_data=["event_date", "event_type","sub_event_type","actor_group","location","fatalities"],
        color="actor_group" if len(st.session_state["countries"]) > 1 else "sub_event_type",
        size_max=20,
        zoom=3,
        mapbox_style='carto-positron',
        title="Event Map",
        height=800,
        width=1800)
    fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    fig_map.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 75
    fig_map.update_geos(projection_type="equirectangular", visible=True, resolution=50)

    chart_dict[0] = fig_map
    return chart_dict

@st.cache_data(hash_funcs={dict: lambda _: None},show_spinner="Generating Plot")
def scatter_map_static(filtered_df):
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        hover_name="event_id_cnty",
        hover_data=["event_date", "event_type","sub_event_type","actor_group","location","fatalities"],
        color="actor_group" if len(st.session_state["countries"]) > 1 else "sub_event_type",
        size_max=20,
        zoom=3,
        mapbox_style="carto-positron",
        title="Event Map",
        height=800,
        width=1800
    )
    chart_dict = {}
    chart_dict[0] = fig_map
    return chart_dict

@st.cache_data(hash_funcs={dict: lambda _: None}, show_spinner = "Generating Plot")
def density_map_anim(density_data):
    chart_dict = {}
    fig_map = px.density_mapbox(
                        density_data.sort_values("event_date").dropna(),
                        lat="latitude",
                        lon="longitude",
                        z = "sub_event_type",
                        animation_frame = "event_date",
                        range_color = (max(1,min(density_data["sub_event_type"].dropna())), max(density_data["sub_event_type"].dropna())),
                        zoom=3,
                        radius=40,
                        mapbox_style="carto-positron",
                        title="Event Map",
                        height=800,
                        width=1800
                    )
    #fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
    #fig_map.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 75
    #fig_map.update_geos(projection_type="equirectangular", visible=True, resolution=50)

    chart_dict[0] = fig_map
    return chart_dict
    
@st.cache_data(hash_funcs={dict: lambda _: None},show_spinner = "Generating Plot")
def density_map_static(density_data):
    fig_map = px.density_mapbox(
                        density_data,
                        lat="latitude",
                        lon="longitude",
                        z = "sub_event_type",
                        zoom=3,
                        radius=40,
                        mapbox_style="carto-positron",
                        title="Event Map",
                        height=800,
                        width=1800
                    )
    chart_dict = {}
    chart_dict[0] = fig_map
    return chart_dict

def line_chart(time_series_df):
    #time_series_df
    fig_time_series = px.line(time_series_df, 
                           x='event_date', 
                           y='event_count', 
                           color=st.session_state["tracking_target_ts"], #'country', 
                           title='Events Over Time',
                           labels={'event_date': 'Date', 'event_count': 'Number of Events'},
                            height=800, width=1800,)
    return fig_time_series

def bar_chart(time_series_df, barmode="group"):
    fig_bar = px.bar(time_series_df,
           x="event_date",
           y="event_count",
           color=st.session_state["tracking_target_ts"],
           title="Bar Chart",
                       barmode = barmode,height=800, width=1800,
           labels={"event_date":"Date","event_count":"Number of Events"})
    return fig_bar

class visualization:
    def __init__(self):
        pass
    

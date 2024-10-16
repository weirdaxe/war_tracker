import pandas as pd
import numpy as np
import streamlit as st
import datetime



class page_elements:
    def __init__(self):
        pass
    
    def sidebar(self,df):
        with st.sidebar:
            st.title("Event Filters", help="Filter the dataset based on various factors. Factors are not applied untill the 'Apply filters' button is pressed")

            countries = st.multiselect("Select countries", options=df['country'].unique(),help="Country where the event happened")
            event_types = st.multiselect("Select event types", options=df["sub_event_type"].unique())
            #try:
            #    actors = st.multiselect("Select Actor", options=st.session_state["filtered_df"]['actor_group'].unique())
            #except:
            actors = st.multiselect("Select Actor", options=df['actor_group'].unique(), help="Actor responsible for the event")
            
            time_range = st.slider("Date Range", min_value = df["event_date"].min().to_pydatetime(), 
                                   max_value = df["event_date"].max().to_pydatetime(),value=(datetime.datetime(2023, 10, 7, 0,0), df["event_date"].max().to_pydatetime()),)
            button = st.button('Apply filters',use_container_width=True)
            st.write("")
            
            st.title("Time Series Analysis")

            st.session_state["time_granularity_ts"] = st.selectbox("Time Granularity",options=["Daily","Weekly", "Monthly","Quarterly","Annually"],key="time_series")
            
            rolling_window_map = {"Daily":(1,30),"Weekly":(1,52), "Monthly":(1,12), "Quarterly":(1,4),"Annually":(1,10)}
            
            
            st.session_state["rolling_window_ts"] = st.slider("Rolling Window (Observations)", rolling_window_map[st.session_state["time_granularity_ts"]][0],rolling_window_map[st.session_state["time_granularity_ts"]][1],key="time_series_rw")
            
            #analysis_dur = st.selectbox("Smoothing time frame", options=["Raw Data", "4 Week", "8 Week", "12 Week"],)

            c1, c2 = st.columns(2)
            with c1:
                tracking = st.selectbox("Value Target",options=["Country","Event Type","Actor"])
                tracking_map = {"Country":"country","Event Type":"sub_event_type", "Actor":"actor_group"}
                st.session_state["tracking_target_ts"] = tracking_map[tracking]
            with c2:
                st.write("")
                st.write("")
                chart_type = st.toggle("Line/Bar")
                st.session_state["chart_type"] = chart_type
            
            #c1,c2 = st.columns([2,1])
            #with c2:
            #    chart_type = st.toggle("Line/Bar")
            #    st.session_state["chart_type"] = chart_type
            #with c1:
            if chart_type: # if bar:
                st.session_state["bar_tpy"] = st.radio("Bar Type",["Bar","Stacked column","Stacked Relative"])
            st.session_state["analysis_tpy"] = st.radio("Analysis",["Raw","Moving Average", "Rolling Sum", "O/O Change","O/O Rolling Change"],)
            st.write("")
            st.write("")
            footer_html = """<div style='text-align: left;'>
              <p>Developed by <b>Matic</b></p>
            </div>"""
            st.markdown(footer_html, unsafe_allow_html=True)
        return button, countries, event_types, actors, time_range
        # if button:
        #     filtered_df = df.copy()
            
        #     st.session_state['countries'] = countries
        #     st.session_state['event_types'] = event_types
        #     st.session_state['actors'] = actors
        #     st.session_state['time_range'] = time_range
            
        #     if countries:
        #         filtered_df = filtered_df[filtered_df['country'].isin(countries)]
        #     if event_types:
        #         filtered_df = filtered_df[filtered_df["sub_event_type"].isin(event_types)]
        #     if actors:
        #         filtered_df = filtered_df[filtered_df['actor_group'].isin(actors)]
        #     if time_range:
        #         filtered_df = filtered_df[(filtered_df['event_date']>=time_range[0]) & (filtered_df['event_date']<=time_range[1])]
        #     st.session_state["filtered_df"] = filtered_df
            #st.success("Filters Applied")
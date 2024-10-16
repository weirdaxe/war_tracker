### App created by weirdaxe for Tracking the Middle East Conflict 
### Distribution not allowed without creator's approval

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from os import listdir
from os.path import isfile, join
import datetime
from PIL import Image

from utils import utils
from visualization import visualization
import visualization as vis
from page_elements import page_elements

u = utils()
v = visualization()
pe = page_elements()

actor_map = mapping = {
    "Protesters (Iran)": "Protestors - Iran",
    "Protesters (Yemen)": "Protestors - Yemen",
    "Unidentified Armed Group (Yemen)": "Yemen - Unidentified Armed Group",
    "Unidentified Armed Group (Israel)": "Israel - Unidentified Armed Group",
    "Military Forces of Israel (2022-)": "Israeli Defense Forces",
    "Hamas Movement": "Hamas",
    "PIJ: Palestinian Islamic Jihad": "Palestinian Islamic Jihad",
    "Rioters (Palestine)": "Protestors - Palestine",
    "Unidentified Armed Group (Palestine)": "Palestine - Unidentified Armed Group",
    "Rioters (Israel)": "Protestors - Israel",
    "Military Forces of Yemen (2017-) Houthi": "Yemen - Houthi",
    "Al Aqsa Martyrs Brigade": "Palestinian Islamic Jihad",
    "Police Forces of Palestine (1994-) West Bank": "Israel - Police",
    "PIJ: Katibat Jenin": "Palestinian Islamic Jihad",
    "Hezbollah": "Hezbollah",
    "Military Forces of Iran (1989-)": "Iran",
    "Police Forces of Iran (1989-) Islamic Republic of Iran Border Guard Command": "Iran - Police",
    "Protesters (Lebanon)": "Protestors - Lebanon",
    "Protesters (Palestine)": "Protestors - Palestine",
    "Protesters (Israel)": "Protestors - Israel",
    "Military Forces of Yemen (2022-) Presidential Leadership Council": "Yemen - Presidential Leadership Council",
    "Military Forces of the United States (2021-)": "United States Military",
    "DFLP: Democratic Front for the Liberation of Palestine": "Palestinian Democratic Front",
    "Mujahideen Brigades": "Yemen - Mujahideen Brigades",
    "Police Forces of Yemen (2017-) Houthi": "Yemen - Police",
    "AAMB: Katibat Tulkarm - Quick Response": "Palestinian Islamic Jihad",
    "Al Nasser Salah al Deen Brigades": "Palestinian Islamic Jihad",
    "West Coast Joint Forces": "Yemen - West Coast Joint Forces",
    "Settlers (Israel)": "Israel - Settlers",
    "Rioters (Yemen)": "Protestors - Yemen",
    "AAMB: Katibat Qalqilya - Quick Response": "Palestinian Islamic Jihad",
    "Rioters (Lebanon)": "Protestors - Lebanon",
    "Military Forces of Yemen (2022-) Presidential Leadership Council - STC Support and Reinforcement Brigades": "Yemen - STC Support",
    "Operation Restoring Hope": "Yemen - Operation Restoring Hope",
    "Unidentified Communal Militia (Yemen)": "Yemen - Unidentified Communal Militia",
    "Unidentified Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Police Forces of Israel (2022-)": "Israel - Police",
    "Rioters (Iran)": "Protestors - Iran",
    "AQAP: Al Qaeda in the Arabian Peninsula": "Al Qaeda",
    "Private Security Forces (Israel)": "Israel - Private Security",
    "Police Forces of Yemen (2022-) Presidential Leadership Council - STC Aden Security": "Yemen - STC Aden Security",
    "PIJ: Katibat Tulkarm": "Palestinian Islamic Jihad",
    "PFLP: Popular Front for the Liberation of Palestine": "Palestinian Popular Front",
    "Police Forces of Palestine (2007-) Gaza Strip": "Israel - Police",
    "Abidah Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Unidentified Armed Group (International)": "International - Unidentified Armed Group",
    "Military Forces of Yemen (2022-) Presidential Leadership Council - STC Shabwani Defense Forces": "Yemen - STC Shabwani Forces",
    "Ansar al Furqan": "Yemen - Ansar al Furqan",
    "Military Forces of Yemen (2022-) Presidential Leadership Council - STC": "Yemen - STC",
    "Military Forces of Iran (1989-) Islamic Revolutionary Guard Corps": "Iran - IRGC",
    "Private Security Forces (International)": "International - Private Security",
    "Military Forces of the United Kingdom (2010-)": "UK Military",
    "Police Forces of Yemen (2022-) Presidential Leadership Council - STC Security Belt Forces": "Yemen - STC Security Belt",
    "AAMB: Katibat Nur ash Shams": "Palestinian Islamic Jihad",
    "Army of Justice": "Yemen - Army of Justice",
    "Police Forces of Iran (1989-)": "Iran - Police",
    "Military Forces of Israel (2022-) Special Forces": "Israeli Defense Forces",
    "Unidentified Military Forces": "Unidentified - Military Forces",
    "Military Forces of Yemen (2022-) Presidential Leadership Council - Nation Shield Forces": "Yemen - Nation Shield Forces",
    "Al Mansur Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Al Azam Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Police Forces of Yemen (2022-) Presidential Leadership Council": "Yemen - Police",
    "Military Forces of France (2017-)": "France Military",
    "Southern Resistance": "Yemen - Southern Resistance",
    "Government of Lebanon (2021-)": "Lebanon - Government",
    "PIJ: Katibat Jericho": "Palestinian Islamic Jihad",
    "Ad Dumayni Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Maqrai Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Khalifah Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Giants Brigades": "Yemen - Giants Brigades",
    "Settlement Emergency Squad": "Israel - Settlement Emergency",
    "Government of Israel (2022-)": "Israel - Government",
    "Unidentified Armed Group (Lebanon)": "Lebanon - Unidentified Armed Group",
    "Police Forces of Yemen (2017-) Houthi - Prison Guards": "Yemen - Police",
    "Al Yaslim Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Unidentified Armed Group (Somalia)": "Somalia - Unidentified Armed Group",
    "Hamas: Kataib Al Ayyash": "Hamas",
    "PIJ: Katibat Tubas": "Palestinian Islamic Jihad",
    "Government of Eritrea (1993-)": "Eritrea - Government",
    "Protesters (Afghanistan)": "Protestors - Afghanistan",
    "Police Forces of Israel (2022-) Prison Guards": "Israel - Police",
    "Al Hamdhan Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Islah Party": "Yemen - Islah Party",
    "Unidentified Armed Group (Iran)": "Iran - Unidentified Armed Group",
    "Protesters (International)": "Protestors - International",
    "PJAK: Kurdistan Free Life Party": "Iran - PJAK",
    "Unidentified Armed Group (Syria)": "Syria - Unidentified Armed Group",
    "Lions' Den": "Palestinian Islamic Jihad",
    "Al Sulaiman Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "PIJ: Katibat Jaba": "Palestinian Islamic Jihad",
    "Military Forces of Lebanon (2021-)": "Lebanon - Military",
    "Al Lahaqad Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Civilians (Lebanon)": "Lebanon - Civilians",
    "Police Forces of Iran (1989-) Ministry of Intelligence": "Iran - Police",
    "Civilians (Palestine)": "Palestine - Civilians",
    "Fatah Movement": "Palestine - Fatah",
    "Police Forces of Yemen (2017-) Houthi - Security and Intelligence Service": "Yemen - Police",
    "PIJ: Katibat Nablus": "Palestinian Islamic Jihad",
    "Az Zubayrat Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Ghurzah Communal Militia (Yemen)": "Yemen - Communal Militia",
    "Police Forces of Israel (2022-) Border Police": "Israel - Police",
    "PIJ: Katibat Hebron": "Palestinian Islamic Jihad",
    "PIJ: Katibat Qabatiyah": "Palestinian Islamic Jihad",
    "Al Dayf Allah Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Hamad Bin Husayn Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Baqatimi Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Military Forces of Saudi Arabia (2015-)": "Saudi Arabia - Military",
    "National Resistance Brigades": "Palestinian Resistance",
    "Al Riyam Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al BuTahif Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Al Jabri Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Unidentified Armed Group (South Sudan)": "South Sudan - Unidentified Armed Group",
    "Unidentified Armed Group (Palestine)": "Palestine - Unidentified Armed Group",
    "Unidentified Armed Group (Turkey)": "Turkey - Unidentified Armed Group",
    "Militia of the Free Syrian Army": "Syria - Free Syrian Army",
    "Unidentified Armed Group (Sudan)": "Sudan - Unidentified Armed Group",
    "SLA: Sudan Liberation Army": "Sudan - Liberation Army",
    "Communal Militia": "Yemen - Communal Militia",
    "Civil Society": "Yemen - Civil Society",
    "Houthi": "Yemen - Houthi",
    "Protesters (Syria)": "Protestors - Syria",
    "Civilians (Iran)": "Iran - Civilians",
    "Civilians (International)": "International - Civilians",
    "AAMB: Katibat Salfit": "Palestinian Islamic Jihad",
    "Jenin Brigades": "Palestinian Islamic Jihad",
    "Protesters (Somalia)": "Protestors - Somalia",
    "Communal Militias": "Yemen - Communal Militias",
    "Unidentified Armed Group (Congo)": "Congo - Unidentified Armed Group",
    "Military Forces of Yemen (2022-) Houthi": "Yemen - Houthi",
    "Protesters (Congo)": "Protestors - Congo",
    "Youth of Palestine": "Palestine - Youth",
    "Community Leaders": "Yemen - Community Leaders",
    "Unidentified Armed Group (Niger)": "Niger - Unidentified Armed Group",
    "Military Forces of the United Nations (2021-)": "UN Peacekeeping Forces",
    "Anarchists (Iran)": "Protestors - Iran",
    "Communal Defense Forces": "Yemen - Communal Defense Forces",
    "Army of Salvation": "Yemen - Army of Salvation",
    "Defense Forces": "Yemen - Defense Forces",
    "Civilians (Lebanon)": "Lebanon - Civilians",
    "Civil Society Organizations": "Yemen - Civil Society Organizations",
    "SLA: Sudan Liberation Army - SPLA": "Sudan - SPLA",
    "Communal Defense Groups": "Yemen - Communal Defense Groups",
    "SLA: Sudan Liberation Army - SLM": "Sudan - SLM",
    "Army of the Revolution": "Yemen - Army of the Revolution",
    "Military Forces of Ethiopia (2021-)": "Ethiopia - Military",
    "SLA: Sudan Liberation Army - SLA": "Sudan - SLA",
    "Al Maamari Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "Civilians (Ethiopia)": "Ethiopia - Civilians",
    "Unidentified Armed Group (Ethiopia)": "Ethiopia - Unidentified Armed Group",
    "Al Malazi Tribal Militia (Yemen)": "Yemen - Tribal Militia",
    "SLA: Sudan Liberation Army - SLAM": "Sudan - SLAM",
}
im = Image.open("media/warfare.ico")
logo = Image.open("media/Logo_large.png")
logo_collapsed = Image.open("media/warfare.png")
st.set_page_config(page_title = "Conflict Tracker", layout="wide", page_icon = im)

st.logo(image=logo, size="large", icon_image=logo_collapsed
)
st.html("""
  <style>
    [alt=Logo] {
        
      height: 5.75rem;
    }
  </style>
        """)

@st.cache_data  # 👈 Add the caching decorator
def load_data(actor_map=actor_map,path = "war_tracker.csv"):
    df = pd.read_csv(path)
    # Convert data types
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    df['actor_group'] = df['actor1'].map(actor_map)
    return df

@st.cache_data(show_spinner="Preparing the Data", persist=True)
def get_data(actor_map=actor_map):
    mypath = "data/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    def safe_eval(text):
        # Replace 'true' with 'True' and 'false' with 'False'
        text = text.replace('true', 'True')
        return text
    
    with open("data/"+onlyfiles[0],"r") as file:
        for line in file:
            line = safe_eval(line)
            df = pd.DataFrame.from_dict(eval(line)["data"])
            
    for file_name in onlyfiles[1:]:
        with open("data/"+file_name, "r") as file:
            for line in file:
                line = safe_eval(line)
                dict_ = eval(line)
        df = pd.concat([df, pd.DataFrame.from_dict(dict_["data"])])
    df = df.reset_index(drop=True)
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    df['actor_group'] = df['actor1'].map(actor_map)
    
    return df

df = get_data()
# filtered_df = df.copy()

# dark_map = datetime.datetime.now().time() > datetime.time(18,0)
# if dark_map:
#     map_col = 'carto-darkmatter'
# else:
#     map_col = 'carto-positron'

# Streamlit App
st.title("Conflict Visualization Dashboard")

if "filtered_df" in st.session_state:
    filtered_df = st.session_state["filtered_df"]


button, countries, event_types, actors, time_range = pe.sidebar(df)

if button:
    filtered_df = df.copy()
    
    st.session_state['countries'] = countries
    st.session_state['event_types'] = event_types
    st.session_state['actors'] = actors
    st.session_state['time_range'] = time_range
    
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    if event_types:
        filtered_df = filtered_df[filtered_df["sub_event_type"].isin(event_types)]
    if actors:
        filtered_df = filtered_df[filtered_df['actor_group'].isin(actors)]
    if time_range:
        filtered_df = filtered_df[(filtered_df['event_date']>=time_range[0]) & (filtered_df['event_date']<=time_range[1])]
    st.session_state["filtered_df"] = filtered_df

#with st.container(height=500,border=False):
try:
# if 1==1:
    breaker = filtered_df.iloc[0,0]
    
    st.subheader("Data Panel")

    dpc1, dpc2 = st.columns([3,2])
    with dpc1:
        with st.container():
            st.write(f"**Total Events:** {str(filtered_df.shape[0])}")
        with st.container():
            c11, c12, c13 = st.columns(3)
            with c11:
                st.write('**Unique Countries:**', str(filtered_df['country'].nunique()))
                st.write(", ".join(filtered_df["country"].unique()))
            with c12:
                st.write('**Unique Event Types:**', str(filtered_df["sub_event_type"].nunique()))
                st.write(", ".join(filtered_df["sub_event_type"].unique()))
            with c13:
                st.write('**Unique Actors:**', str(filtered_df['actor_group'].nunique()))
                st.write(", ".join(filtered_df['actor_group'].unique()))

        
        # Event type distribution
        st.subheader('Event Type Distribution')
        event_type_counts = filtered_df.groupby(["country","sub_event_type"]).size().reset_index(name="event_count")#["sub_event_type"].value_counts()
        st.bar_chart(event_type_counts, y= "event_count", x="sub_event_type", color="country",
                     horizontal=True,stack=True,x_label="Event Count",y_label="Event Type")

    with dpc2:
        # Pie Chart if only 1 country selected
        if len(st.session_state['countries'])==1:
            # Generate Pie Chart with type of event in %
            if len(st.session_state['event_types']) ==1:
                # Generate chart base on perpitrator groups
                fig_pie = px.pie(u.aggregate_events(filtered_df.groupby(['actor_group']).size().reset_index(name="value"), threshold = 0.01,group="actor_group"), 
                 values='value', names='actor_group', title='Actor Breakdown')
            else:
                # Generate chart based on event types
                fig_pie = px.pie(u.aggregate_events(filtered_df.groupby(["sub_event_type"]).size().reset_index(name="value"),threshold=0.01,group="sub_event_type"), 
                 values='value', names='sub_event_type', title='Event Breakdown')
        else:
            # Plot events by country                                ["sub_event_type"].count()
            fig_pie = px.pie(u.aggregate_events(filtered_df.groupby(["country"]).size().reset_index(name="value"),threshold=0.01, group="country"), 
                 values='value', names='country', title='Activity in Countries')
            
        st.plotly_chart(fig_pie)
    st.divider()
    # Map Visualization
    col1, col2, col3 = st.columns([5,2,2])
    with col1:
        st.subheader("Event Map View")
    with col2:
        anim_tog = st.toggle("Static / Animated")
    with col3:
        dens_tog = st.toggle("Events / Density")
    if not dens_tog:
        if not anim_tog:
            if not filtered_df.empty: 
                fig_map_static = vis.scatter_map_static(filtered_df)
                st.plotly_chart(fig_map_static[0])    
        if anim_tog:
            if not filtered_df.empty:
                fig_map_anim = vis.scatter_map_anim(filtered_df)
                st.plotly_chart(fig_map_anim[0])
    
    @st.cache_data(show_spinner = "Preparing Data")
    def prep_data(df,area_size_km = 10, time=False):
        return u.geo_group(df, area_size_km = area_size_km, time=time)

    @st.cache_data(show_spinner = "Wrangling Data")
    def fil_data(df,rolling_window=1,time_gran="Daily"):
        return u.geo_filter(df, rolling_window, time_gran)
    
    if dens_tog:
        area_size = st.slider("Select Grouped Area (km) for density calculation.",1, 100, 10, help="""Aggregate events by distance.\nIf 10 is selected this will look for and sum the number of events in a 10x10 km area.\nLower for more granularity, higher for more of a highlevel overview""")

        if not anim_tog:
            if not filtered_df.empty:
                density_data = prep_data(filtered_df, area_size_km = area_size, time=False)
                fig_density_map_static = vis.density_map_static(density_data)
                st.plotly_chart(fig_density_map_static[0])
 
        if anim_tog:
            st.session_state["time_granularity_map"] = st.selectbox("Time Granularity",options=["Daily","Weekly", "Monthly","Annually"], key="map", help="Select the unit of time, events are summed up")
            rolling_window_map = {"Daily":(1,30),"Weekly":(1,52), "Monthly":(1,12), "Quarterly":(1,4),"Annually":(1,10)}
            st.session_state["rolling_window_map"] = st.slider("Rolling Window (Observations)", rolling_window_map[st.session_state["time_granularity_map"]][0],rolling_window_map[st.session_state["time_granularity_map"]][1],key="map_rw", help="Select the rolling window, the calculation is a rolling sum")
            
            if not filtered_df.empty:
                density_data = prep_data(filtered_df, area_size_km = area_size, time=True)
                density_data = fil_data(density_data,rolling_window=st.session_state["rolling_window_map"],time_gran=st.session_state["time_granularity_map"])
                fig_density_map_anim = vis.density_map_anim(density_data)
                st.plotly_chart(fig_density_map_anim[0])
 
    st.divider()
    st.subheader("Time Series View")
    
    #@st.cache_data
    def ts_df(filtered_df):
        return filtered_df.groupby(['event_date', st.session_state["tracking_target_ts"]]).size().reset_index(name="event_count")
                                    #'country',"actor_group","sub_event_type"]).size().reset_index(name='event_count')
    
    time_series_df = ts_df(filtered_df)
    # Prepare time series data
    #time_series_df = filtered_df.groupby(['event_date', 'country']).size().reset_index(name='event_count')

    if st.session_state["time_granularity_ts"] == "Weekly":
        #time_series_df.groupby("country").resample("D",on="event_date").size().reset_index(name="event_count")
        time_series_df = time_series_df.groupby(st.session_state["tracking_target_ts"]).resample("W-MON",on="event_date").sum()["event_count"].reset_index()
    
    elif st.session_state["time_granularity_ts"] == "Monthly":
        time_series_df = time_series_df.groupby(st.session_state["tracking_target_ts"]).resample("ME",on="event_date").sum()["event_count"].reset_index()
    
    elif st.session_state["time_granularity_ts"] == "Quarterly":
        time_series_df = time_series_df.groupby(st.session_state["tracking_target_ts"]).resample("Q",on="event_date",).sum()["event_count"].reset_index()
    
    elif st.session_state["time_granularity_ts"] == "Annually":
        time_series_df = time_series_df.groupby(st.session_state["tracking_target_ts"]).resample("Y",on="event_date").sum()["event_count"].reset_index()
    
  
    # Resampling based on analysis type
    if st.session_state["analysis_tpy"] == "Moving Average":
        if st.session_state["rolling_window_ts"] != 1:
            time_series_df["event_count"] = time_series_df.groupby(st.session_state["tracking_target_ts"])['event_count'].transform(lambda x: x.rolling(window=st.session_state["rolling_window_ts"]).mean())
    
    if st.session_state["analysis_tpy"] == "Rolling Sum":
        if st.session_state["rolling_window_ts"] != 1:
            time_series_df["event_count"] = time_series_df.groupby(st.session_state["tracking_target_ts"])['event_count'].transform(lambda x: x.rolling(window=st.session_state["rolling_window_ts"]).sum())

    if st.session_state["analysis_tpy"] == "O/O Change":
        if st.session_state["rolling_window_ts"] != 1:
            time_series_df = u.calculate_pct_change(time_series_df, window=st.session_state["rolling_window_ts"], use_rolling_sum=False)
    
    if st.session_state["analysis_tpy"] == "O/O Rolling Change":
        if st.session_state["rolling_window_ts"] != 1:
            time_series_df = u.calculate_pct_change(time_series_df, window=st.session_state["rolling_window_ts"], use_rolling_sum=True)
    
    if not st.session_state["chart_type"]:        
        fig_ts_line = vis.line_chart(time_series_df)
        st.plotly_chart(fig_ts_line)
    
    if st.session_state["chart_type"]:
        if st.session_state["bar_tpy"] == "Bar":
            fig_ts_bar = vis.bar_chart(time_series_df, barmode="group")
        
        elif st.session_state["bar_tpy"] == "Stacked column":
            fig_ts_bar = vis.bar_chart(time_series_df, barmode="relative")
        
        elif st.session_state["bar_tpy"] == "Stacked Relative":
            time_series_df = u.make_ts_relative(time_series_df)
            fig_ts_bar = vis.bar_chart(time_series_df, barmode="relative")
        else:
            pass
        st.plotly_chart(fig_ts_bar)

except:
    st.info("Please select your filters and click apply")
else:
    st.write("No data available for the selected filters.")

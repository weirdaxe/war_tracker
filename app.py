### App created by weirdaxe for Tracking the Middle East Conflict 
### Distribution not allowed without creator's approval

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from os import listdir
from os.path import isfile, join
import datetime

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

st.set_page_config(layout="wide")
@st.cache_data  # 👈 Add the caching decorator
def load_data(actor_map=actor_map,path = "war_tracker.csv"):
    df = pd.read_csv(path)
    # Convert data types
    df['event_date'] = pd.to_datetime(df['event_date'])
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    df['actor_group'] = df['actor1'].map(actor_map)
    return df

#df = load_data()

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
#df.to_csv("war_tracker.csv")

df = get_data()
filtered_df = df.copy()

dark_map = datetime.datetime.now().time() > datetime.time(18,0)
if dark_map:
    map_col = 'carto-darkmatter'
else:
    map_col = 'carto-positron'

# Streamlit App
st.title("Matic's Middle East Event Visualization Dashboard")

# Multi-select for countries
countries = st.multiselect("Select countries", options=filtered_df['country'].unique())

if countries:
    filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    
# Multi-select for event types
event_types = st.multiselect("Select event types", options=filtered_df['event_type'].unique())

if event_types:
    filtered_df = filtered_df[filtered_df['event_type'].isin(event_types)]
    
actors = st.multiselect("Select Actor", options=filtered_df['actor_group'].unique())

if actors:
    filtered_df = filtered_df[filtered_df['actor_group'].isin(actors)]

def calculate_pct_change(df, window=1, use_rolling_sum=False):
    if use_rolling_sum:
        # Calculate rolling sum for the specified window
        df['event_count'] = df.groupby('country')['event_count'].transform(lambda x: x.rolling(window).sum())
        # Calculate percentage change between the last 'window' sum and the sum before that
        df['event_count'] = df.groupby('country')['event_count'].transform(lambda x: x.pct_change(periods=window))
    else:
        # Calculate percentage change with the specified window
        df['event_count'] = df.groupby('country')['event_count'].transform(lambda x: x.pct_change(periods=window))
    return df

# Map Visualization
st.subheader("Event Map")
map_tog = st.toggle("Static / Animated")
if map_tog:
    if not filtered_df.empty:
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="latitude",
            lon="longitude",
            animation_frame = "event_date",
            hover_name="event_id_cnty",
            hover_data=["event_date", "event_type","actor_group"],
            color="country" if len(countries) > 1 else "event_type",
            size_max=20,
            zoom=4,
            mapbox_style='carto-positron',
            title="Event Map",
            height=800,
            width = 1800
        )
        fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 150
        fig_map.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
        fig_map.update_geos(resolution=50)
        st.plotly_chart(fig_map)
if not map_tog:
    if not filtered_df.empty:
        fig_map = px.scatter_mapbox(
            filtered_df,
            lat="latitude",
            lon="longitude",
            hover_name="event_id_cnty",
            hover_data=["event_date", "event_type","actor_group"],
            color="country" if len(countries) > 1 else "event_type",
            size_max=20,
            zoom=4,
            mapbox_style='carto-positron',
            title="Event Map",
            height=800,
            width = 1800
        )
        st.plotly_chart(fig_map)

    # Time Series Line Chart
    st.subheader("Time Series of Events")
    
    # Selector for moving average or rolling sum
    analysis_dur = st.selectbox("Select analysis type", options=["Raw Data", "4 Week", "8 Week", "12 Week"],)
    analysis_tpy = st.radio("Analysis",["Raw","Moving Average", "Rolling Sum", "W/W Change","M/M Rolling Change"],)
       
    # Prepare time series data
    time_series_df = filtered_df.groupby(['event_date', 'country']).size().reset_index(name='event_count')

    # Resampling based on analysis type
    if analysis_tpy == "Moving Average":
        if analysis_dur == "4 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=4).mean())
        elif analysis_dur == "8 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=8).mean())
        elif analysis_dur == "12 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=12).mean())
        else:
            pass
    
    if analysis_tpy == "Rolling Sum":
        if analysis_dur == "4 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=4).sum())
        elif analysis_dur == "8 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=8).sum())
        elif analysis_dur == "12 Week":
            time_series_df["event_count"] = time_series_df.groupby('country')['event_count'].transform(lambda x: x.rolling(window=12).sum())
        else:
            pass

    if analysis_tpy == "M/M Change":
        if analysis_dur == "Raw":
            time_series_df = calculate_pct_change(time_series_df, window=1, use_rolling_sum=False)
        elif analysis_dur == "4 Week":
            time_series_df = calculate_pct_change(time_series_df, window=4, use_rolling_sum=False)
        elif analysis_dur == "8 Week":
            time_series_df = calculate_pct_change(time_series_df, window=8, use_rolling_sum=False)
        elif analysis_dur == "12 Week":
            time_series_df = calculate_pct_change(time_series_df, window=12, use_rolling_sum=False)
        else:
            pass

    if analysis_tpy == "M/M Rolling Change":
        if analysis_dur == "Raw":
            time_series_df = calculate_pct_change(time_series_df, window=1, use_rolling_sum=True)
        elif analysis_dur == "4 Week":
            time_series_df = calculate_pct_change(time_series_df, window=4, use_rolling_sum=True)
        elif analysis_dur == "8 Week":
            time_series_df = calculate_pct_change(time_series_df, window=8, use_rolling_sum=True)
        elif analysis_dur == "12 Week":
            time_series_df = calculate_pct_change(time_series_df, window=12, use_rolling_sum=True)
        else:
            pass
            

    # Plotting
    fig_time_series = px.line(time_series_df, 
                               x='event_date', 
                               y='event_count', 
                               color='country', 
                               title='Events Over Time', height=800, width=1800,
                               labels={'event_date': 'Date', 'event_count': 'Number of Events'})
    
    # Show the plot
    st.plotly_chart(fig_time_series)

else:
    st.write("No data available for the selected filters.")

import pandas as pd
import numpy as np
import streamlit as st

class utils:

    def __init__(self):
        pass

    def aggregate_events(self, data, threshold = 0.03, group="actor_group"):
        # Calculate the total sum of the 'value' column
        total_sum = data['value'].sum()
        threshold = threshold * total_sum  # 3% of the total sum
    
        # Filter rows that meet the threshold
        filtered_data = data[data['value'] > threshold]
    
        # Get rows that don't meet the threshold
        others_data = data[data['value'] <= threshold]
    
        # Aggregate the 'Others' rows
        if not others_data.empty:
            others_value = others_data['value'].sum()
            others_row = pd.DataFrame({group: ['Others'], 'value': [others_value]})
            # Combine the filtered data with the 'Others' row
            result = pd.concat([filtered_data, others_row], ignore_index=True)
        else:
            result = filtered_data
    
        return result

    def calculate_pct_change(self, df, window=1, use_rolling_sum=False):
        if use_rolling_sum:
            # Calculate rolling sum for the specified window
            df['event_count'] = df.groupby(st.session_state["tracking_target_ts"])['event_count'].transform(lambda x: x.rolling(window).sum())
            # Calculate percentage change between the last 'window' sum and the sum before that
            df['event_count'] = df.groupby(st.session_state["tracking_target_ts"])['event_count'].transform(lambda x: x.pct_change(periods=window))
        else:
            # Calculate percentage change with the specified window
            df['event_count'] = df.groupby(st.session_state["tracking_target_ts"])['event_count'].transform(lambda x: x.pct_change(periods=window))
        return df

    def geo_time_filter(self, df, frequency):
        # Convert relevant columns to numpy arrays
        latitudes = df['latitude'].to_numpy()
        longitudes = df['longitude'].to_numpy()
        event_dates = pd.to_datetime(df['event_date']).to_numpy()
        sub_event_types = df['sub_event_type'].to_numpy()
        
        # Create a structured array for easy manipulation
        data = np.array(list(zip(latitudes, longitudes, event_dates, sub_event_types)),
                        dtype=[('latitude', 'f4'), ('longitude', 'f4'), ('event_date', f'datetime64[{frequency}]'), ('sub_event_type', 'i4')])
        
        # Sort the data by latitude, longitude, and event_date
        data.sort(order=['latitude', 'longitude', 'event_date'])
        
        # Use numpy to aggregate data
        unique_indices = np.unique(data[['latitude', 'longitude', 'event_date']], axis=0, return_index=True)[1]
        aggregated_data = []
        
        for idx in unique_indices:
            current_lat = data[idx]['latitude']
            current_lon = data[idx]['longitude']
            current_month = data[idx]['event_date']
            
            # Get the mask for the same latitude, longitude, and month
            mask = (data['latitude'] == current_lat) & (data['longitude'] == current_lon) & (data['event_date'] == current_month)
            
            # Sum the sub_event_type where the mask is True
            total_sub_event_type = np.sum(data['sub_event_type'][mask])
            
            # Only append if the sum is greater than zero
            if total_sub_event_type > 0:
                aggregated_data.append((current_lat, current_lon, current_month, total_sub_event_type))
        
        # Convert the results to a structured numpy array or a DataFrame
        result_array = np.array(aggregated_data, dtype=[('latitude', 'f4'), ('longitude', 'f4'), ('event_date', f'datetime64[{frequency}]'), ('sub_event_type', 'i4')])
        
        # Convert to DataFrame if needed
        result_df = pd.DataFrame(result_array)
        return (result_df)
    
    def geo_filter(self, df, rolling_window=1, time_gran="Daily"):
        # With Density DataFrame
        if time_gran == "Weekly":
            df = self.geo_time_filter(df, "W")
            #df.groupby("sub_event_type").resample("W-MON",on="event_date").sum()["event_count"].reset_index()
        elif time_gran == "Monthly":
            df = self.geo_time_filter(df, "M")
        
        elif time_gran == "Annually":
            df = self.geo_time_filter(df, "Y")
            
        if rolling_window != 1:
            df["sub_event_type"] = df.groupby(["latitude","longitude"])["sub_event_type"].transform(lambda x: x.rolling(window=rolling_window).sum())

        return df
    
    def geo_group(self, df, area_size_km = 10,time=False):
        # Define constants
        dy, dx = area_size_km/2, area_size_km/2
        
        r_earth = 6371
        pi = np.pi
        if not time:
            df_gb = df.groupby(["latitude","longitude"])["sub_event_type"].count().reset_index()
        if time:
            df_gb = df.groupby(["latitude","longitude","event_date"])["sub_event_type"].count().reset_index()
            event_dates = df_gb["event_date"].to_numpy()
            
        # Convert DataFrame to NumPy arrays
        latitudes = df_gb["latitude"].to_numpy()
        longitudes = df_gb["longitude"].to_numpy()
        event_types = df_gb["sub_event_type"].to_numpy()  # Get event types
        
        # Pre-compute bounding boxes
        lat_min = latitudes - (dy / r_earth) * (180 / np.pi)
        lat_max = latitudes + (dy / r_earth) * (180 / np.pi)
        long_min = longitudes - (dx / r_earth) * (180 / np.pi) / np.cos(np.radians(latitudes))
        long_max = longitudes + (dx / r_earth) * (180 / np.pi) / np.cos(np.radians(latitudes))
        
        # Initialize an array to store counts
        event_counts = np.zeros(len(latitudes), dtype=int)
        
        # Iterate over the bounding boxes and count efficiently
        for i in range(len(latitudes)):
            # Filter based on latitude first
            lat_mask = (latitudes >= lat_min[i]) & (latitudes <= lat_max[i])
            filtered_longitudes = longitudes[lat_mask]
            filtered_event_types = event_types[lat_mask]
            if time:
                filtered_dates = event_dates[lat_mask]  # Get corresponding event dates
                
            # Count using a boolean mask for the filtered longitudes
            if len(filtered_longitudes) > 0:
                long_mask = (filtered_longitudes >= long_min[i]) & (filtered_longitudes <= long_max[i])
                if time:
                    same_date_mask = (filtered_dates == event_dates[i])
                    event_counts[i] = int(np.sum(filtered_event_types[long_mask & same_date_mask])) 
                else:
                    event_counts[i] = np.sum(filtered_event_types[long_mask])
        df_gb["sub_event_type"] = event_counts
        return df_gb

    def make_ts_relative(self, time_series_df):
        time_series_df = time_series_df.pivot_table(index='event_date', columns=st.session_state["tracking_target_ts"], values='event_count', aggfunc='sum', fill_value=0)
        time_series_df = time_series_df.div(time_series_df.sum(axis=1), axis=0).reset_index()
        time_series_df = time_series_df.melt(id_vars='event_date', var_name=st.session_state["tracking_target_ts"], value_name='event_count')
        time_series_df["event_count"] = time_series_df["event_count"] * 100
        return time_series_df

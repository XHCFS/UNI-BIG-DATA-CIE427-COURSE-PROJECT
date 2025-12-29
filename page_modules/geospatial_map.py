"""
Geospatial Map Page - Interactive climate station map.
"""

import streamlit as st
from api import fetch_api_data, safe_get
import pandas as pd
import pydeck as pdk


def render():
    """Render the Geospatial Map page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #0369a1;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-map-marked-alt"></i> Geospatial Climate Map</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Interactive map view of climate station data
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get global parameters
    server_address = st.session_state.get('server_address', '152.53.160.43:8000')
    start_year = st.session_state.get('start_year', 1950)
    end_year = st.session_state.get('end_year', 2019)
    country_prefix = st.session_state.get('country_prefix', 'FR')
    
    # Controls row
    col1, col2 = st.columns([2, 2])
    
    with col1:
        metric = st.selectbox(
            "Metric",
            options=["Temperature", "Precipitation", "Snow Depth"],
            index=0
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch data
    params = {
        'country_prefix': country_prefix,
        'start_year': start_year,
        'end_year': end_year
    }
    
    data = fetch_api_data(server_address, 'map', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/geospatial/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # Display map
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #0ea5e9; padding-left: 1rem;'>
            <i class="fas fa-map-marker-alt"></i> Station Locations
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        stations = safe_get(data, 'stations', default=[])
        
        if stations:
            # Create DataFrame for map
            map_data = []
            for station in stations:
                lat = station.get('latitude')
                lon = station.get('longitude')
                
                if lat is not None and lon is not None:
                    map_data.append({
                        'lat': lat,
                        'lon': lon,
                        'station_id': station.get('station_id', ''),
                        'name': station.get('name', ''),
                        'avg_temp': station.get('avg_temp'),
                        'total_precip': station.get('total_precip'),
                        'avg_snow_depth': station.get('avg_snow_depth')
                    })
            
            if map_data:
                df = pd.DataFrame(map_data)
                
                # Fill NaN values in numeric columns
                df['avg_temp'] = df['avg_temp'].fillna(0)
                df['total_precip'] = df['total_precip'].fillna(0)
                df['avg_snow_depth'] = df['avg_snow_depth'].fillna(0)
                
                # Prepare color based on metric
                if metric == "Temperature" and 'avg_temp' in df.columns:
                    # Normalize temperature for color mapping (heatmap effect)
                    temp_min = df['avg_temp'].min()
                    temp_max = df['avg_temp'].max()
                    metric_min = temp_min
                    metric_max = temp_max
                    df['color_value'] = df['avg_temp']
                    df['display_value'] = df['avg_temp'].round(1).astype(str) + '°C'
                    
                    # Create RGB colors based on temperature (blue to red)
                    if temp_max > temp_min:
                        df['normalized'] = (df['avg_temp'] - temp_min) / (temp_max - temp_min)
                    else:
                        df['normalized'] = 0.5
                    
                    df['normalized'] = df['normalized'].fillna(0.5)
                    df['red'] = (df['normalized'] * 255).fillna(128).astype(int)
                    df['blue'] = ((1 - df['normalized']) * 255).fillna(128).astype(int)
                    df['green'] = 100
                elif metric == "Precipitation" and 'total_precip' in df.columns:
                    # Normalize precipitation for gradient (light to dark green)
                    precip_min = df['total_precip'].min()
                    precip_max = df['total_precip'].max()
                    metric_min = precip_min
                    metric_max = precip_max
                    df['color_value'] = df['total_precip']
                    df['display_value'] = df['total_precip'].round(1).astype(str) + ' mm'
                    
                    # Create gradient from light green to dark green
                    if precip_max > precip_min:
                        df['normalized'] = (df['total_precip'] - precip_min) / (precip_max - precip_min)
                    else:
                        df['normalized'] = 0.5
                    
                    df['normalized'] = df['normalized'].fillna(0.5)
                    df['red'] = (16 + df['normalized'] * 0).fillna(16).astype(int)
                    df['green'] = (100 + df['normalized'] * 155).fillna(128).astype(int)
                    df['blue'] = (50 + df['normalized'] * 79).fillna(90).astype(int)
                elif metric == "Snow Depth" and 'avg_snow_depth' in df.columns:
                    # Normalize snow depth for gradient (light to dark purple)
                    snow_min = df['avg_snow_depth'].min()
                    snow_max = df['avg_snow_depth'].max()
                    metric_min = snow_min
                    metric_max = snow_max
                    df['color_value'] = df['avg_snow_depth']
                    df['display_value'] = df['avg_snow_depth'].round(1).astype(str) + ' cm'
                    
                    # Create gradient from light purple to dark purple
                    if snow_max > snow_min:
                        df['normalized'] = (df['avg_snow_depth'] - snow_min) / (snow_max - snow_min)
                    else:
                        df['normalized'] = 0.5
                    
                    df['normalized'] = df['normalized'].fillna(0.5)
                    df['red'] = (180 - df['normalized'] * 41).fillna(160).astype(int)
                    df['green'] = (150 - df['normalized'] * 58).fillna(120).astype(int)
                    df['blue'] = (255 - df['normalized'] * 9).fillna(246).astype(int)
                else:
                    df['color_value'] = 0
                    df['display_value'] = '--'
                    df['red'] = 100
                    df['green'] = 100
                    df['blue'] = 100
                    metric_min = 0
                    metric_max = 0
                
                # Create pydeck layer with tooltips
                layer = pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[lon, lat]',
                    get_color='[red, green, blue, 200]',
                    get_radius=20000,
                    pickable=True,
                    auto_highlight=True,
                )
                
                # Set the view state
                view_state = pdk.ViewState(
                    latitude=df['lat'].mean(),
                    longitude=df['lon'].mean(),
                    zoom=5,
                    pitch=0,
                )
                
                # Create the deck
                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip={
                        'html': '<b>Station:</b> {station_id}<br/>'
                                '<b>Name:</b> {name}<br/>'
                                '<b>' + metric + ':</b> {display_value}<br/>'
                                '<b>Lat:</b> {lat}<br/>'
                                '<b>Lon:</b> {lon}',
                        'style': {
                            'backgroundColor': 'steelblue',
                            'color': 'white'
                        }
                    }
                )
                
                # Create columns for map and legend
                col_map, col_legend = st.columns([8, 1])
                
                with col_map:
                    st.pydeck_chart(deck)
                
                with col_legend:
                    # Show color legend for selected metric
                    if metric == "Temperature":
                        st.markdown("**Temperature**")
                        st.markdown(f"<div style='background: linear-gradient(to bottom, rgb(255, 0, 0), rgb(255, 100, 0), rgb(191, 100, 64), rgb(128, 100, 128), rgb(64, 64, 191), rgb(0, 0, 255)); padding: 20px 10px; text-align: center; border-radius: 5px; color: white; font-weight: bold; height: 400px; display: flex; flex-direction: column; justify-content: space-between;'><div>{metric_max:.1f}°C</div><div style='flex-grow: 1;'></div><div>{metric_min:.1f}°C</div></div>", unsafe_allow_html=True)
                        st.caption("Hot → Cold")
                    elif metric == "Precipitation":
                        st.markdown("**Precipitation**")
                        st.markdown(f"<div style='background: linear-gradient(to bottom, rgb(16, 255, 129), rgb(16, 185, 129), rgb(16, 120, 90), rgb(16, 100, 50)); padding: 20px 10px; text-align: center; border-radius: 5px; color: white; font-weight: bold; height: 400px; display: flex; flex-direction: column; justify-content: space-between;'><div>{metric_max:.1f} mm</div><div style='flex-grow: 1;'></div><div>{metric_min:.1f} mm</div></div>", unsafe_allow_html=True)
                        st.caption("High → Low")
                    elif metric == "Snow Depth":
                        st.markdown("**Snow Depth**")
                        st.markdown(f"<div style='background: linear-gradient(to bottom, rgb(180, 150, 255), rgb(139, 92, 246), rgb(110, 70, 220), rgb(80, 50, 200)); padding: 20px 10px; text-align: center; border-radius: 5px; color: white; font-weight: bold; height: 400px; display: flex; flex-direction: column; justify-content: space-between;'><div>{metric_max:.1f} cm</div><div style='flex-grow: 1;'></div><div>{metric_min:.1f} cm</div></div>", unsafe_allow_html=True)
                        st.caption("High → Low")
                
                # Show station count
                st.markdown(f"**{len(map_data)} stations** displayed")
                
                # Show station details table
                with st.expander("View Station Details"):
                    display_df = df[['station_id', 'name', 'lat', 'lon', 'avg_temp', 'total_precip', 'avg_snow_depth']].copy()
                    display_df = display_df.rename(columns={
                        'station_id': 'Station ID',
                        'name': 'Name',
                        'lat': 'Latitude',
                        'lon': 'Longitude',
                        'avg_temp': 'Avg Temp (°C)',
                        'total_precip': 'Total Precip (mm)',
                        'avg_snow_depth': 'Avg Snow (cm)'
                    })
                    st.dataframe(display_df, use_container_width=True)
            else:
                st.warning("No valid coordinates found in station data")
        else:
            st.warning("No station data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

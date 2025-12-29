"""
Trends & Time Series Page - Temporal climate patterns.
"""

import streamlit as st
from api import fetch_api_data, safe_get
from components import create_line_chart_data
import pandas as pd


def render():
    """Render the Trends & Time Series page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #0e7490;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-chart-line"></i> Trends & Time Series</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Climate trends and temporal patterns over time
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get global parameters
    server_address = st.session_state.get('server_address', '152.53.160.43:8000')
    start_year = st.session_state.get('start_year', 1950)
    end_year = st.session_state.get('end_year', 2019)
    country_prefix = st.session_state.get('country_prefix', 'FR')
    
    # Top-right toggles
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col2:
        include_outliers = st.checkbox("Include Outliers", value=True)
    
    with col3:
        mark_thresholds = st.checkbox("Mark Thresholds", value=False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch data
    params = {
        'country_prefix': country_prefix,
        'start_year': start_year,
        'end_year': end_year
    }
    
    data = fetch_api_data(server_address, 'trends', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/trends/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # Temperature chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #ef4444; padding-left: 1rem;'>
            <i class="fas fa-temperature-high"></i> Temperature Trends
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        # Series toggles
        temp_series = st.multiselect(
            "Select series to display",
            options=["Min Temp", "Max Temp"],
            default=["Min Temp", "Max Temp"],
            key="temp_series"
        )
        
        # Get temperature data
        data_points = safe_get(data, 'data_points', 'temperature', default=[])
        
        if data_points:
            # Filter outliers if needed
            if not include_outliers:
                # Filter out extreme values (999.0 sentinel)
                filtered_points = [
                    p for p in data_points 
                    if (p.get('avg_tmin') != 999.0 and p.get('avg_tmax') != 999.0)
                ]
            else:
                filtered_points = data_points
            
            # Create DataFrame
            df = pd.DataFrame(filtered_points)
            
            if not df.empty and 'timestamp' in df.columns:
                df['timestamp'] = df['timestamp'].astype(str)
                df = df.set_index('timestamp')
                
                # Select columns based on user selection
                cols_to_plot = []
                if "Min Temp" in temp_series and 'avg_tmin' in df.columns:
                    cols_to_plot.append('avg_tmin')
                if "Max Temp" in temp_series and 'avg_tmax' in df.columns:
                    cols_to_plot.append('avg_tmax')
                
                if cols_to_plot:
                    plot_df = df[cols_to_plot].copy()
                    
                    # Rename columns for display
                    plot_df = plot_df.rename(columns={
                        'avg_tmin': 'Min Temp',
                        'avg_tmax': 'Max Temp'
                    })
                    
                    # Replace None/999.0 with NaN for better plotting
                    plot_df = plot_df.replace([999.0, -999.0], float('nan'))
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    
                    # Add traces based on selected series
                    if 'Min Temp' in plot_df.columns:
                        fig.add_trace(go.Scatter(
                            x=plot_df.index,
                            y=plot_df['Min Temp'],
                            mode='lines',
                            name='Min Temp',
                            line=dict(color='#3b82f6', width=2),
                            hovertemplate='Year: %{x}<br>Min Temp: %{y}°C<extra></extra>'
                        ))
                    
                    if 'Max Temp' in plot_df.columns:
                        fig.add_trace(go.Scatter(
                            x=plot_df.index,
                            y=plot_df['Max Temp'],
                            mode='lines',
                            name='Max Temp',
                            line=dict(color='#ef4444', width=2),
                            hovertemplate='Year: %{x}<br>Max Temp: %{y}°C<extra></extra>'
                        ))
                    
                    fig.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=10, b=10),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        xaxis=dict(
                            title='Year',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        yaxis=dict(
                            title='Temperature (°C)',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        plot_bgcolor='rgba(250,250,250,0.5)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if mark_thresholds:
                        st.info("Threshold markers: Min Temp < 0°C (Cold), Max Temp > 30°C (Hot)")
                else:
                    st.warning("Please select at least one temperature series")
            else:
                st.warning("No temperature data available")
        else:
            st.warning("No temperature data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Precipitation chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #10b981; padding-left: 1rem;'>
            <i class="fas fa-tint"></i> Precipitation Trends
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        # Get precipitation data from data_points
        precip_data_points = safe_get(data, 'data_points', 'precipitation', default=[])
        
        if precip_data_points:
            df = pd.DataFrame(precip_data_points)
            
            if not df.empty and 'timestamp' in df.columns:
                df['timestamp'] = df['timestamp'].astype(str)
                df = df.set_index('timestamp')
                
                # Check for precipitation field
                if 'total_precip' in df.columns:
                    plot_df = df[['total_precip']].copy()
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=plot_df.index,
                        y=plot_df['total_precip'],
                        mode='lines',
                        line=dict(color='#10b981', width=2),
                        hovertemplate='Year: %{x}<br>Precipitation: %{y} mm<extra></extra>'
                    ))
                    fig.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=10, b=10),
                        showlegend=False,
                        xaxis=dict(
                            title='Year',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        yaxis=dict(
                            title='Precipitation (mm)',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        plot_bgcolor='rgba(250,250,250,0.5)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Precipitation field not found in data")
            else:
                st.warning("No valid precipitation data structure")
        else:
            st.info("Precipitation data not available in trends endpoint")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Snow depth chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #8b5cf6; padding-left: 1rem;'>
            <i class="fas fa-snowflake"></i> Snow Depth Trends
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        # Try to get snow depth from different possible locations in the response
        snow_data_points = safe_get(data, 'data_points', 'snow_depth', default=[]) or \
                          safe_get(data, 'data_points', 'snow', default=[]) or \
                          safe_get(data, 'data_points', 'snowfall', default=[])
        
        if snow_data_points:
            df = pd.DataFrame(snow_data_points)
            
            if not df.empty and 'timestamp' in df.columns:
                df['timestamp'] = df['timestamp'].astype(str)
                df = df.set_index('timestamp')
                
                # Check for snow depth field with different possible names
                snow_field = None
                for field in ['avg_snow_depth', 'snow_depth', 'avg_snow', 'snowfall']:
                    if field in df.columns:
                        snow_field = field
                        break
                
                if snow_field:
                    plot_df = df[[snow_field]].copy()
                    
                    # Filter out sentinel values
                    plot_df = plot_df.replace([999.0, -999.0], float('nan'))
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=plot_df.index,
                        y=plot_df[snow_field],
                        mode='lines',
                        line=dict(color='#8b5cf6', width=2),
                        hovertemplate='Year: %{x}<br>Snow Depth: %{y} cm<extra></extra>'
                    ))
                    fig.update_layout(
                        height=400,
                        margin=dict(l=10, r=10, t=10, b=10),
                        showlegend=False,
                        xaxis=dict(
                            title='Year',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        yaxis=dict(
                            title='Snow Depth (cm)',
                            showgrid=True,
                            gridcolor='rgba(200,200,200,0.2)'
                        ),
                        plot_bgcolor='rgba(250,250,250,0.5)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Snow depth field not found in data. Available fields: " + ", ".join(df.columns.tolist()))
            else:
                st.warning("No valid snow data structure")
        else:
            st.info("Snow depth data not available in trends endpoint")
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

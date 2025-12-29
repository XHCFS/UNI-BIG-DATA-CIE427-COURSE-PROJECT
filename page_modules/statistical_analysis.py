"""
Statistical Analysis Page - Statistics and distributions.
"""

import streamlit as st
from api import fetch_api_data, safe_get, format_number
from components import render_stats_card


def render():
    """Render the Statistical Analysis page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #6d28d9;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-chart-bar"></i> Statistical Analysis</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Statistics and distributions
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get global parameters
    server_address = st.session_state.get('server_address', '152.53.160.43:8000')
    start_year = st.session_state.get('start_year', 1950)
    end_year = st.session_state.get('end_year', 2019)
    country_prefix = st.session_state.get('country_prefix', 'FR')
    
    # Fetch data
    params = {
        'country_prefix': country_prefix,
        'start_year': start_year,
        'end_year': end_year
    }
    
    data = fetch_api_data(server_address, 'statistics', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/statistics/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # Stats cards row: 5 cards
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #8b5cf6; padding-left: 1rem;'>
            <i class="fas fa-chart-bar"></i> Statistical Indicators
        </h3>
    """, unsafe_allow_html=True)
    
    stat_indicators = safe_get(data, 'stat_indicators', default={})
    
    # Define color schemes for different stat types
    stat_colors = {
        'mean': {
            'bg': 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
            'border': '#3b82f6',
            'text': '#1e3a8a',
            'text_secondary': '#1e40af',
            'shadow': 'rgba(59, 130, 246, 0.2)'
        },
        'median': {
            'bg': 'linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%)',
            'border': '#8b5cf6',
            'text': '#581c87',
            'text_secondary': '#6b21a8',
            'shadow': 'rgba(139, 92, 246, 0.2)'
        },
        'std': {
            'bg': 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
            'border': '#f59e0b',
            'text': '#92400e',
            'text_secondary': '#b45309',
            'shadow': 'rgba(245, 158, 11, 0.2)'
        },
        'skew': {
            'bg': 'linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)',
            'border': '#ea580c',
            'text': '#7c2d12',
            'text_secondary': '#9a3412',
            'shadow': 'rgba(234, 88, 12, 0.2)'
        },
        'range': {
            'bg': 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
            'border': '#10b981',
            'text': '#065f46',
            'text_secondary': '#047857',
            'shadow': 'rgba(16, 185, 129, 0.2)'
        }
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Mean
    with col1:
        mean_data = stat_indicators.get('mean', {})
        temp_mean = format_number(mean_data.get('mean_temp_min'), 2, "°C")
        precip_mean = format_number(mean_data.get('mean_precip'), 2, "mm")
        snow_mean = format_number(mean_data.get('mean_snow'), 2, "cm")
        
        render_stats_card("Mean", temp_mean, precip_mean, snow_mean, color_scheme=stat_colors['mean'])
    
    # Median (may need to calculate or use mean as fallback)
    with col2:
        median_data = stat_indicators.get('median', {})
        if not median_data:
            # Fallback to mean if median not available
            median_data = mean_data
        
        temp_median = format_number(median_data.get('median_temp_min') or median_data.get('mean_temp_min'), 2, "°C")
        precip_median = format_number(median_data.get('median_precip') or median_data.get('mean_precip'), 2, "mm")
        snow_median = format_number(median_data.get('median_snow') or median_data.get('mean_snow'), 2, "cm")
        
        render_stats_card("Median", temp_median, precip_median, snow_median, color_scheme=stat_colors['median'])
    
    # Standard Deviation
    with col3:
        std_data = stat_indicators.get('std', {})
        temp_std = format_number(std_data.get('std_temp_min'), 2, "°C")
        precip_std = format_number(std_data.get('std_precip'), 2, "mm")
        snow_std = format_number(std_data.get('std_snow'), 2, "cm")
        
        render_stats_card("Std Dev", temp_std, precip_std, snow_std, color_scheme=stat_colors['std'])
    
    # Skewness
    with col4:
        skew_data = stat_indicators.get('skewness', {})
        temp_skew = format_number(skew_data.get('skew_temp_min'), 2, "")
        precip_skew = format_number(skew_data.get('skew_precip'), 2, "")
        snow_skew = format_number(skew_data.get('skew_snow'), 2, "")
        
        render_stats_card("Skewness", temp_skew, precip_skew, snow_skew, color_scheme=stat_colors['skew'])
    
    # Range
    with col5:
        range_data = stat_indicators.get('range', {})
        
        temp_range = range_data.get('range_temp_min', {})
        temp_range_str = f"{format_number(temp_range.get('start'), 1)} to {format_number(temp_range.get('end'), 1)}"
        
        precip_range = range_data.get('range_precip', {})
        precip_range_str = f"{format_number(precip_range.get('start'), 1)} to {format_number(precip_range.get('end'), 1)}"
        
        snow_range = range_data.get('range_snow', {})
        snow_range_str = f"{format_number(snow_range.get('start'), 1)} to {format_number(snow_range.get('end'), 1)}"
        
        render_stats_card("Range", temp_range_str, precip_range_str, snow_range_str, color_scheme=stat_colors['range'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Temperature histograms from trends data
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #ef4444; padding-left: 1rem;'>
            <i class="fas fa-temperature-high"></i> Temperature Distributions
        </h3>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;'>
            Distribution of yearly average temperatures across the selected time period
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch trends data to get yearly temperature values
    trends_data = fetch_api_data(server_address, 'trends', params)
    
    col1, col2 = st.columns(2)
    
    if trends_data:
        temp_data_points = safe_get(trends_data, 'data_points', 'temperature', default=[])
        
        if temp_data_points:
            import pandas as pd
            import plotly.graph_objects as go
            df = pd.DataFrame(temp_data_points)
            
            with col1:
                st.markdown("#### Maximum Temperature")
                with st.container(border=True):
                    if 'avg_tmax' in df.columns:
                        values = df['avg_tmax'].dropna()
                        # Filter sentinel values
                        values = values[(values != 999.0) & (values != -999.0)]
                        
                        if len(values) > 0:
                            # Create histogram with plotly for better control
                            fig = go.Figure()
                            fig.add_trace(go.Histogram(
                                x=values,
                                nbinsx=15,
                                marker=dict(color='#ef4444', line=dict(color='rgba(0,0,0,0.2)', width=1)),
                                hovertemplate='Temperature: %{x}°C<br>Count: %{y}<extra></extra>'
                            ))
                            fig.update_layout(
                                height=350,
                                margin=dict(l=10, r=10, t=10, b=10),
                                showlegend=False,
                                xaxis=dict(
                                    title='Temperature (°C)',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                yaxis=dict(
                                    title='Frequency',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                plot_bgcolor='rgba(250,250,250,0.5)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No valid temperature data")
                    else:
                        st.info("Maximum temperature field not found")
            
            with col2:
                st.markdown("#### Minimum Temperature")
                with st.container(border=True):
                    if 'avg_tmin' in df.columns:
                        values = df['avg_tmin'].dropna()
                        # Filter sentinel values
                        values = values[(values != 999.0) & (values != -999.0)]
                        
                        if len(values) > 0:
                            # Create histogram with plotly for better control
                            fig = go.Figure()
                            fig.add_trace(go.Histogram(
                                x=values,
                                nbinsx=15,
                                marker=dict(color='#3b82f6', line=dict(color='rgba(0,0,0,0.2)', width=1)),
                                hovertemplate='Temperature: %{x}\u00b0C<br>Count: %{y}<extra></extra>'
                            ))
                            fig.update_layout(
                                height=350,
                                margin=dict(l=10, r=10, t=10, b=10),
                                showlegend=False,
                                xaxis=dict(
                                    title='Temperature (\u00b0C)',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                yaxis=dict(
                                    title='Frequency',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                plot_bgcolor='rgba(250,250,250,0.5)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No valid temperature data")
                    else:
                        st.info("Minimum temperature field not found")
        else:
            with col1:
                st.markdown("#### Maximum Temperature")
                with st.container(border=True):
                    st.info("Temperature data not available")
            with col2:
                st.markdown("#### Minimum Temperature")
                with st.container(border=True):
                    st.info("Temperature data not available")
    else:
        with col1:
            st.markdown("#### Maximum Temperature")
            with st.container(border=True):
                st.info("Unable to fetch trends data")
        with col2:
            st.markdown("#### Minimum Temperature")
            with st.container(border=True):
                st.info("Unable to fetch trends data")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Precipitation and Snow Depth histograms
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #10b981; padding-left: 1rem;'>
             Precipitation & Snow Depth Distributions
        </h3>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;'>
            Distribution of yearly values across the selected time period
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if trends_data:
        with col1:
            st.markdown("#### Precipitation Distribution")
            with st.container(border=True):
                precip_data_points = safe_get(trends_data, 'data_points', 'precipitation', default=[])
                
                if precip_data_points:
                    df_precip = pd.DataFrame(precip_data_points)
                    
                    if 'total_precip' in df_precip.columns:
                        values = df_precip['total_precip'].dropna()
                        # Filter sentinel values and zeros
                        values = values[(values != 999.0) & (values != -999.0) & (values > 0)]
                        
                        if len(values) > 0:
                            # Create histogram with plotly
                            fig = go.Figure()
                            fig.add_trace(go.Histogram(
                                x=values,
                                nbinsx=15,
                                marker=dict(color='#10b981', line=dict(color='rgba(0,0,0,0.2)', width=1)),
                                hovertemplate='Precipitation: %{x} mm<br>Count: %{y}<extra></extra>'
                            ))
                            fig.update_layout(
                                height=350,
                                margin=dict(l=10, r=10, t=10, b=10),
                                showlegend=False,
                                xaxis=dict(
                                    title='Precipitation (mm)',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                yaxis=dict(
                                    title='Frequency',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                plot_bgcolor='rgba(250,250,250,0.5)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No valid precipitation data")
                    else:
                        st.info("Precipitation field not found")
                else:
                    st.info("Precipitation data not available")
        
        with col2:
            st.markdown("#### Snow Depth Distribution")
            with st.container(border=True):
                # Try to get snow data from trends endpoint - check snow_depth first
                snow_data_points = safe_get(trends_data, 'data_points', 'snow_depth', default=[]) or \
                                  safe_get(trends_data, 'data_points', 'snow', default=[]) or \
                                  safe_get(trends_data, 'data_points', 'temperature', default=[])
                
                if snow_data_points:
                    df_snow = pd.DataFrame(snow_data_points)
                    
                    # Look for snow depth field
                    snow_field = None
                    for field in ['avg_snow_depth', 'snow_depth', 'avg_snow']:
                        if field in df_snow.columns:
                            snow_field = field
                            break
                    
                    if snow_field:
                        values = df_snow[snow_field].dropna()
                        # Filter sentinel values
                        values = values[(values != 999.0) & (values != -999.0) & (values >= 0)]
                        
                        if len(values) > 0:
                            # Create histogram with plotly
                            fig = go.Figure()
                            fig.add_trace(go.Histogram(
                                x=values,
                                nbinsx=15,
                                marker=dict(color='#8b5cf6', line=dict(color='rgba(0,0,0,0.2)', width=1)),
                                hovertemplate='Snow Depth: %{x} cm<br>Count: %{y}<extra></extra>'
                            ))
                            fig.update_layout(
                                height=350,
                                margin=dict(l=10, r=10, t=10, b=10),
                                showlegend=False,
                                xaxis=dict(
                                    title='Snow Depth (cm)',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                yaxis=dict(
                                    title='Frequency',
                                    showgrid=True,
                                    gridcolor='rgba(200,200,200,0.2)'
                                ),
                                plot_bgcolor='rgba(250,250,250,0.5)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No valid snow depth data")
                    else:
                        st.info("Snow depth field not found. Available fields: " + ", ".join(df_snow.columns.tolist()))
                else:
                    st.info("Snow depth data not available")
    else:
        with col1:
            st.markdown("#### Precipitation Distribution")
            with st.container(border=True):
                st.info("Unable to fetch trends data")
        with col2:
            st.markdown("#### Snow Depth Distribution")
            with st.container(border=True):
                st.info("Unable to fetch trends data")
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

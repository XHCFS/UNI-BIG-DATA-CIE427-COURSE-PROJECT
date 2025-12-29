"""
Seasonal Patterns Page - Monthly and seasonal climate analysis.
"""

import streamlit as st
from api import fetch_api_data, safe_get, format_number
from components import render_seasonal_card
import pandas as pd
import plotly.graph_objects as go


def render():
    """Render the Seasonal Patterns page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #047857;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-leaf"></i> Seasonal Patterns</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Monthly and seasonal climate analysis
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
    
    data = fetch_api_data(server_address, 'seasons', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/seasons/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # Seasonal summary row
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #10b981; padding-left: 1rem;'>
            <i class="fas fa-leaf"></i> Seasonal Summary
        </h3>
    """, unsafe_allow_html=True)
    
    seasonal_summary = safe_get(data, 'seasonal_summary', default={})
    
    # Define seasonal color schemes
    season_colors = {
        'spring': {
            'bg': 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
            'border': '#10b981',
            'text': '#065f46',
            'text_secondary': '#047857',
            'shadow': 'rgba(16, 185, 129, 0.2)',
            'bar_color': '#10b981'
        },
        'summer': {
            'bg': 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
            'border': '#f59e0b',
            'text': '#92400e',
            'text_secondary': '#b45309',
            'shadow': 'rgba(245, 158, 11, 0.2)',
            'bar_color': '#f59e0b'
        },
        'autumn': {
            'bg': 'linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)',
            'border': '#ea580c',
            'text': '#7c2d12',
            'text_secondary': '#9a3412',
            'shadow': 'rgba(234, 88, 12, 0.2)',
            'bar_color': '#ea580c'
        },
        'winter': {
            'bg': 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
            'border': '#3b82f6',
            'text': '#1e3a8a',
            'text_secondary': '#1e40af',
            'shadow': 'rgba(59, 130, 246, 0.2)',
            'bar_color': '#3b82f6'
        }
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    seasons = [
        ('Spring', 'spring', col1),
        ('Summer', 'summer', col2),
        ('Autumn', 'autumn', col3),
        ('Winter', 'winter', col4)
    ]
    
    for season_name, season_key, col in seasons:
        with col:
            season_data = seasonal_summary.get(season_key, {})
            avg_temp = season_data.get('avg_temp')
            temp_range = season_data.get('temp_range', {})
            temp_min = temp_range.get('min')
            temp_max = temp_range.get('max')
            total_precip = season_data.get('total_precip')
            avg_snow = season_data.get('avg_snow_depth')
            
            render_seasonal_card(
                season_name,
                avg_temp,
                (temp_min, temp_max),
                total_precip,
                avg_snow,
                color_scheme=season_colors[season_key]
            )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monthly temperature charts
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #f59e0b; padding-left: 1rem;'>
            <i class="fas fa-temperature-high"></i> Monthly Temperature Patterns
        </h3>
    """, unsafe_allow_html=True)
    
    monthly_data = safe_get(data, 'monthly_data', default=[])
    
    if monthly_data:
        df = pd.DataFrame(monthly_data)
        
        if 'month' in df.columns:
            # Create month names
            month_names = {
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
            }
            
            df['month_name'] = df['month'].map(month_names)
            df = df.set_index('month_name')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Min/Max Temperature per Month")
                with st.container(border=True):
                    if 'avg_tmin' in df.columns and 'avg_tmax' in df.columns:
                        # Define month to season mapping and colors
                        month_to_season = {
                            'Jan': 'winter', 'Feb': 'winter', 'Mar': 'spring',
                            'Apr': 'spring', 'May': 'spring', 'Jun': 'summer',
                            'Jul': 'summer', 'Aug': 'summer', 'Sep': 'autumn',
                            'Oct': 'autumn', 'Nov': 'autumn', 'Dec': 'winter'
                        }
                        
                        # Create colors for each month based on season
                        month_colors_min = [season_colors[month_to_season[month]]['bar_color'] for month in df.index]
                        month_colors_max = [season_colors[month_to_season[month]]['bar_color'] for month in df.index]
                        
                        # Create plotly figure for side-by-side bars
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=df.index,
                            y=df['avg_tmin'],
                            name='Min Temp (°C)',
                            marker=dict(
                                color='#3b82f6',
                                line=dict(color='#1e40af', width=1.5)
                            ),
                            hovertemplate='<b>Min Temp</b><br>Month: %{x}<br>Temp: %{y:.1f}°C<extra></extra>'
                        ))
                        fig.add_trace(go.Bar(
                            x=df.index,
                            y=df['avg_tmax'],
                            name='Max Temp (°C)',
                            marker=dict(
                                color='#ef4444',
                                line=dict(color='#b91c1c', width=1.5)
                            ),
                            hovertemplate='<b>Max Temp</b><br>Month: %{x}<br>Temp: %{y:.1f}°C<extra></extra>'
                        ))
                        fig.update_layout(
                            barmode='group',
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
                                title='Month',
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
                    else:
                        st.warning("Min/Max temperature fields not found")
            
            with col2:
                st.markdown("#### Average Precipitation per Month")
                with st.container(border=True):
                    if 'total_precip' in df.columns:
                        # Create plotly figure to match temperature chart height
                        fig_precip = go.Figure()
                        fig_precip.add_trace(go.Bar(
                            x=df.index,
                            y=df['total_precip'],
                            marker=dict(color='#10b981', line=dict(color='rgba(0,0,0,0.2)', width=1)),
                            hovertemplate='<b>Precipitation</b><br>Month: %{x}<br>Amount: %{y} mm<extra></extra>'
                        ))
                        fig_precip.update_layout(
                            height=400,
                            margin=dict(l=10, r=10, t=10, b=10),
                            showlegend=False,
                            xaxis=dict(
                                title='Month',
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
                        st.plotly_chart(fig_precip, use_container_width=True)
                    else:
                        st.warning("Precipitation field not found")
        else:
            st.warning("Month field not found in monthly data")
    else:
        st.warning("No monthly data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monthly average temperature chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #f59e0b; padding-left: 1rem;'>
            <i class="fas fa-temperature-high"></i> Average Temperature per Month
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        if monthly_data:
            df = pd.DataFrame(monthly_data)
            
            if 'month' in df.columns and 'avg_temp' in df.columns:
                # Create month names
                month_names = {
                    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                }
                
                df['month_name'] = df['month'].map(month_names)
                df = df.set_index('month_name')
                
                # Create plotly bar chart with axis labels
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    x=df.index,
                    y=df['avg_temp'],
                    marker=dict(
                        color='#f59e0b',
                        line=dict(color='#d97706', width=1.5)
                    ),
                    hovertemplate='<b>Avg Temperature</b><br>Month: %{x}<br>Temp: %{y:.1f}°C<extra></extra>'
                ))
                fig_bar.update_layout(
                    height=400,
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=False,
                    xaxis=dict(
                        title='Month',
                        showgrid=True,
                        gridcolor='rgba(200,200,200,0.2)'
                    ),
                    yaxis=dict(
                        title='Average Temperature (°C)',
                        showgrid=True,
                        gridcolor='rgba(200,200,200,0.2)'
                    ),
                    plot_bgcolor='rgba(250,250,250,0.5)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Required fields not found in monthly data")
        else:
            st.warning("No monthly data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monthly details table
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #06b6d4; padding-left: 1rem;'>
            <i class="fas fa-clipboard-list"></i> Monthly Details
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .stDataFrame {
                border: 2px solid #06b6d4 !important;
                border-radius: 8px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        if monthly_data:
            df = pd.DataFrame(monthly_data)
            
            if 'month' in df.columns:
                display_df = df[[
                    'month', 'avg_tmin', 'avg_tmax', 'avg_temp',
                    'total_precip', 'avg_snow_depth', 'season'
                ]].copy() if all(col in df.columns for col in ['month', 'avg_tmin', 'avg_tmax', 'avg_temp', 'total_precip', 'avg_snow_depth', 'season']) else df
                
                if not display_df.empty:
                    display_df = display_df.rename(columns={
                        'month': 'Month',
                        'avg_tmin': 'Min Temp (°C)',
                        'avg_tmax': 'Max Temp (°C)',
                        'avg_temp': 'Avg Temp (°C)',
                        'total_precip': 'Precipitation (mm)',
                        'avg_snow_depth': 'Snow Depth (cm)',
                        'season': 'Season'
                    })
                    
                    st.dataframe(display_df, use_container_width=True)
                else:
                    st.warning("No data to display")
            else:
                st.warning("Month field not found in monthly data")
        else:
            st.warning("No monthly data available")
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

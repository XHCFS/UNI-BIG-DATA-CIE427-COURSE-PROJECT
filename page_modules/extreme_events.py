"""
Extreme Events Page - Detection and analysis of climate extremes.
"""

import streamlit as st
import streamlit.components.v1 as components
from api import fetch_api_data, safe_get
from components import render_event_kpi_card
import pandas as pd
import plotly.graph_objects as go


def render():
    """Render the Extreme Events page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #991b1b;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-exclamation-triangle"></i> Extreme Events Analysis</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Detection and analysis of climate extremes
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
    
    data = fetch_api_data(server_address, 'extreme_events', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/extreme_events/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # KPI row: 4 cards
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #dc2626; padding-left: 1rem;'>
            <i class="fas fa-chart-bar"></i> Event Counts
        </h3>
    """, unsafe_allow_html=True)
    
    # Define color schemes for each event type
    event_colors = {
        'heatwave': {
            'bg': 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
            'border': '#ef4444',
            'text': '#7f1d1d',
            'text_secondary': '#991b1b',
            'shadow': 'rgba(239, 68, 68, 0.2)'
        },
        'coldwave': {
            'bg': 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
            'border': '#3b82f6',
            'text': '#1e3a8a',
            'text_secondary': '#1e40af',
            'shadow': 'rgba(59, 130, 246, 0.2)'
        },
        'precipitation': {
            'bg': 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
            'border': '#10b981',
            'text': '#065f46',
            'text_secondary': '#047857',
            'shadow': 'rgba(16, 185, 129, 0.2)'
        },
        'snowfall': {
            'bg': 'linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%)',
            'border': '#8b5cf6',
            'text': '#581c87',
            'text_secondary': '#6b21a8',
            'shadow': 'rgba(139, 92, 246, 0.2)'
        }
    }
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        heatwave_data = safe_get(data, 'heatwave', default={})
        heatwave_count = heatwave_data.get('total_count', 0)
        # Get last date from most_recent if available
        most_recent = heatwave_data.get('most_recent', {})
        last_date = most_recent.get('date', '')
        
        render_event_kpi_card('<i class="fas fa-temperature-high"></i> Heatwaves', heatwave_count, last_date, color_scheme=event_colors['heatwave'])
    
    with col2:
        coldwave_data = safe_get(data, 'coldwave', default={})
        coldwave_count = coldwave_data.get('total_count', 0)
        most_recent = coldwave_data.get('most_recent', {})
        last_date = most_recent.get('date', '')
        
        render_event_kpi_card('<i class="fas fa-snowflake"></i> Cold Waves', coldwave_count, last_date, color_scheme=event_colors['coldwave'])
    
    with col3:
        precip_data = safe_get(data, 'heavy_precipitation', default={})
        precip_count = precip_data.get('total_count', 0)
        most_recent = precip_data.get('most_recent', {})
        last_date = most_recent.get('date', '')
        
        render_event_kpi_card('<i class="fas fa-tint"></i> Heavy Precipitation', precip_count, last_date, color_scheme=event_colors['precipitation'])
    
    with col4:
        snow_data = safe_get(data, 'heavy_snowfall', default={})
        snow_count = snow_data.get('total_count', 0)
        most_recent = snow_data.get('most_recent', {})
        last_date = most_recent.get('date', '')
        
        render_event_kpi_card('<i class="fas fa-snowflake"></i> Heavy Snowfall', snow_count, last_date, color_scheme=event_colors['snowfall'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Event Counts chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #f59e0b; padding-left: 1rem;'>
            <i class="fas fa-chart-line"></i> Event Counts Over Time
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        # Series selection
        event_series = st.multiselect(
            "Select events to display",
            options=["Heatwave", "Cold Wave", "Precipitation", "Snowfall"],
            default=["Heatwave", "Cold Wave"],
            key="event_series"
        )
        
        # Combine yearly data from all event types
        all_years = {}
        
        if "Heatwave" in event_series:
            for item in heatwave_data.get('yearly_counts', []):
                year = str(item.get('year', ''))
                if year:
                    if year not in all_years:
                        all_years[year] = {}
                    all_years[year]['<i class="fas fa-temperature-high"></i> Heatwave'] = item.get('count', 0)
        
        if "Cold Wave" in event_series:
            for item in coldwave_data.get('yearly_counts', []):
                year = str(item.get('year', ''))
                if year:
                    if year not in all_years:
                        all_years[year] = {}
                    all_years[year]['<i class="fas fa-snowflake"></i> Cold Wave'] = item.get('count', 0)
        
        if "Precipitation" in event_series:
            for item in precip_data.get('yearly_counts', []):
                year = str(item.get('year', ''))
                if year:
                    if year not in all_years:
                        all_years[year] = {}
                    all_years[year]['<i class="fas fa-tint"></i> Precipitation'] = item.get('count', 0)
        
        if "Snowfall" in event_series:
            for item in snow_data.get('yearly_counts', []):
                year = str(item.get('year', ''))
                if year:
                    if year not in all_years:
                        all_years[year] = {}
                    all_years[year]['<i class="fas fa-cloud-snow"></i> Snowfall'] = item.get('count', 0)
        
        if all_years:
            df = pd.DataFrame.from_dict(all_years, orient='index')
            df.index.name = 'Year'
            df = df.fillna(0)
            
            # Create plotly figure for side-by-side bars
            fig = go.Figure()
            
            color_map = {
                '<i class="fas fa-temperature-high"></i> Heatwave': '#ef4444',
                '<i class="fas fa-snowflake"></i> Cold Wave': '#3b82f6',
                '<i class="fas fa-tint"></i> Precipitation': '#10b981',
                '<i class="fas fa-cloud-snow"></i> Snowfall': '#8b5cf6'
            }
            
            for col in df.columns:
                fig.add_trace(go.Bar(
                    x=df.index,
                    y=df[col],
                    name=col,
                    marker=dict(
                        color=color_map.get(col, '#666666'),
                        line=dict(color='rgba(0,0,0,0.2)', width=1)
                    ),
                    hovertemplate='<b>' + col + '</b><br>Year: %{x}<br>Count: %{y}<extra></extra>'
                ))
            
            fig.update_layout(
                barmode='group',
                height=450,
                margin=dict(l=10, r=10, t=30, b=10),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#fbbf24",
                    borderwidth=2
                ),
                xaxis=dict(
                    title="Year",
                    showgrid=True,
                    gridcolor='rgba(251,191,36,0.1)'
                ),
                yaxis=dict(
                    title="Event Count",
                    showgrid=True,
                    gridcolor='rgba(251,191,36,0.1)'
                ),
                plot_bgcolor='rgba(255,251,235,0.3)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least one event type to display chart")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Extreme Events Table
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #8b5cf6; padding-left: 1rem;'>
            <i class="fas fa-clipboard-list"></i> Recent Extreme Events
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .stDataFrame {
                border: 2px solid #8b5cf6 !important;
                border-radius: 8px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        # Create a table from the available extreme event data
        events_list = []
        
        # Add heatwave events from yearly data
        heatwave_yearly = heatwave_data.get('yearly_counts', [])
        for year_data in heatwave_yearly[-10:]:  # Last 10 years
            if year_data.get('count', 0) > 0:
                events_list.append({
                    'Date': str(year_data.get('year', '')),
                    'Event Type': 'Heatwave',
                    'Count': year_data.get('count', 0)
                })
        
        # Add coldwave events from yearly data
        coldwave_yearly = coldwave_data.get('yearly_counts', [])
        for year_data in coldwave_yearly[-10:]:  # Last 10 years
            if year_data.get('count', 0) > 0:
                events_list.append({
                    'Date': str(year_data.get('year', '')),
                    'Event Type': 'Cold Wave',
                    'Count': year_data.get('count', 0)
                })
        
        # Add precipitation events from yearly data
        precip_yearly = precip_data.get('yearly_counts', [])
        for year_data in precip_yearly[-10:]:  # Last 10 years
            if year_data.get('count', 0) > 0:
                events_list.append({
                    'Date': str(year_data.get('year', '')),
                    'Event Type': 'Heavy Precipitation',
                    'Count': year_data.get('count', 0)
                })
        
        # Add snowfall events from yearly data
        snow_yearly = snow_data.get('yearly_counts', [])
        for year_data in snow_yearly[-10:]:  # Last 10 years
            if year_data.get('count', 0) > 0:
                events_list.append({
                    'Date': str(year_data.get('year', '')),
                    'Event Type': 'Heavy Snowfall',
                    'Count': year_data.get('count', 0)
                })
        
        if events_list:
            events_df = pd.DataFrame(events_list)
            # Sort by date descending
            events_df = events_df.sort_values('Date', ascending=False)
            
            st.dataframe(
                events_df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
        else:
            st.info("No extreme event records available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

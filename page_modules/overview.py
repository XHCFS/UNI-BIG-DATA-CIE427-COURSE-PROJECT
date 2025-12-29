"""
Overview Page - Climate Overview with KPIs and extreme events.
"""

import streamlit as st
from api import fetch_api_data, safe_get, format_number
from components import render_kpi_card, render_extreme_event_row
import json


def render():
    """Render the Overview page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #ea580c;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-globe"></i> Climate Overview</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                High-level summary and key climate metrics
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
    
    data = fetch_api_data(server_address, 'overview', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/overview/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # KPI Grid: 2 rows × 3 columns
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #f59e0b; padding-left: 1rem;'>
            <i class="fas fa-bolt"></i> Key Climate Metrics
        </h3>
    """, unsafe_allow_html=True)
    
    # Row 1
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        avg_max_temp = safe_get(data, 'temperature', 'avg_max_temp')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); 
                        border-radius: 10px; border: 2px solid #f87171; box-shadow: 0 2px 8px rgba(248,113,113,0.2);'>
                <div style='color: #991b1b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-temperature-high"></i> AVG MAXIMUM TEMP</div>
                <div style='color: #7f1d1d; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(avg_max_temp, 2, "°C")), unsafe_allow_html=True)
    
    with col2:
        avg_min_temp = safe_get(data, 'temperature', 'avg_min_temp')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        border-radius: 10px; border: 2px solid #3b82f6; box-shadow: 0 2px 8px rgba(59,130,246,0.2);'>
                <div style='color: #1e3a8a; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-snowflake"></i> AVG MINIMUM TEMP</div>
                <div style='color: #1e40af; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(avg_min_temp, 2, "°C")), unsafe_allow_html=True)
    
    with col3:
        extreme_events_count = safe_get(data, 'extreme_events_count')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        border-radius: 10px; border: 2px solid #fbbf24; box-shadow: 0 2px 8px rgba(251,191,36,0.2);'>
                <div style='color: #92400e; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-exclamation-triangle"></i> EXTREME EVENTS</div>
                <div style='color: #78350f; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(extreme_events_count, 0, "")), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        total_precip = safe_get(data, 'total_precipitation')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                        border-radius: 10px; border: 2px solid #10b981; box-shadow: 0 2px 8px rgba(16,185,129,0.2);'>
                <div style='color: #065f46; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-tint"></i> TOTAL PRECIPITATION</div>
                <div style='color: #064e3b; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(total_precip, 2, "mm")), unsafe_allow_html=True)
    
    with col2:
        avg_snow = safe_get(data, 'avg_snow_depth')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); 
                        border-radius: 10px; border: 2px solid #8b5cf6; box-shadow: 0 2px 8px rgba(139,92,246,0.2);'>
                <div style='color: #6b21a8; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-snowflake"></i> AVG SNOW DEPTH</div>
                <div style='color: #581c87; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(avg_snow, 2, "cm")), unsafe_allow_html=True)
    
    with col3:
        coverage = safe_get(data, 'coverage')
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        border-radius: 10px; border: 2px solid #3b82f6; box-shadow: 0 2px 8px rgba(59,130,246,0.2);'>
                <div style='color: #1e3a8a; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-check"></i> DATA COVERAGE</div>
                <div style='color: #1e40af; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(coverage, 2, "%")), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top Extremes section
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #ef4444; padding-left: 1rem;'>
            <i class="fas fa-fire"></i> Top Extreme Events
        </h3>
    """, unsafe_allow_html=True)
    
    extreme_events = safe_get(data, 'extreme_events', default={})
    
    # Hottest day
    hottest = extreme_events.get('hottest_day', {})
    hottest_temp = hottest.get('temperature')
    hottest_date = hottest.get('date', '--')
    
    # Filter sentinel values (999, -999)
    if hottest_temp and hottest_temp not in [999, -999, 999.0, -999.0]:
        hottest_temp_str = format_number(hottest_temp, 1, "°C")
    else:
        hottest_temp_str = '--'
    
    # Coldest day
    coldest = extreme_events.get('coldest_day', {})
    coldest_temp = coldest.get('temperature')
    coldest_date = coldest.get('date', '--')
    
    # Filter sentinel values
    if coldest_temp and coldest_temp not in [999, -999, 999.0, -999.0]:
        coldest_temp_str = format_number(coldest_temp, 1, "°C")
    else:
        coldest_temp_str = '--'
    
    # Heaviest precipitation - try multiple possible field names
    heaviest_precip = extreme_events.get('heaviest_precipitation', {}) or extreme_events.get('heaviest_day', {})
    precip_amount = heaviest_precip.get('precipitation') or heaviest_precip.get('amount')
    precip_date = heaviest_precip.get('date', '--')
    precip_amount_str = format_number(precip_amount, 1, "mm") if precip_amount else '--'
    
    # Largest snowfall - try multiple possible field names
    largest_snow = extreme_events.get('largest_snowfall', {}) or extreme_events.get('heaviest_snowfall', {})
    snow_amount = largest_snow.get('snowfall') or largest_snow.get('snow_depth') or largest_snow.get('depth') or largest_snow.get('amount')
    snow_date = largest_snow.get('date', '--')
    snow_amount_str = format_number(snow_amount, 1, "cm") if snow_amount else '--'
    
    # Row 1: Hottest and Coldest
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
            <div style='padding: 2rem; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); 
                        border-radius: 12px; border: 2px solid #ef4444; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);'>
                <div style='color: #7f1d1d; font-size: 1rem; font-weight: 700; margin-bottom: 1rem;'><i class="fas fa-temperature-high"></i> Hottest Day</div>
                <div style='color: #991b1b; font-size: 0.9rem; margin-bottom: 0.5rem;'>{hottest_date}</div>
                <div style='color: #ef4444; font-size: 2.5rem; font-weight: 700;'>{hottest_temp_str}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='padding: 2rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        border-radius: 12px; border: 2px solid #3b82f6; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);'>
                <div style='color: #1e3a8a; font-size: 1rem; font-weight: 700; margin-bottom: 1rem;'><i class="fas fa-snowflake"></i> Coldest Day</div>
                <div style='color: #1e40af; font-size: 0.9rem; margin-bottom: 0.5rem;'>{coldest_date}</div>
                <div style='color: #3b82f6; font-size: 2.5rem; font-weight: 700;'>{coldest_temp_str}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Precipitation and Snowfall
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
            <div style='padding: 2rem; background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                        border-radius: 12px; border: 2px solid #10b981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);'>
                <div style='color: #065f46; font-size: 1rem; font-weight: 700; margin-bottom: 1rem;'><i class="fas fa-cloud-rain"></i> Heaviest Precipitation</div>
                <div style='color: #047857; font-size: 0.9rem; margin-bottom: 0.5rem;'>{precip_date}</div>
                <div style='color: #10b981; font-size: 2.5rem; font-weight: 700;'>{precip_amount_str}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='padding: 2rem; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); 
                        border-radius: 12px; border: 2px solid #8b5cf6; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);'>
                <div style='color: #581c87; font-size: 1rem; font-weight: 700; margin-bottom: 1rem;'><i class="fas fa-cloud-snow"></i> Largest Snowfall</div>
                <div style='color: #6b21a8; font-size: 0.9rem; margin-bottom: 0.5rem;'>{snow_date}</div>
                <div style='color: #8b5cf6; font-size: 2.5rem; font-weight: 700;'>{snow_amount_str}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

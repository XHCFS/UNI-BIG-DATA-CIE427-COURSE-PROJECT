"""
Climate Comparisons Page - Side-by-side comparison of two countries.
"""

import streamlit as st
from api import fetch_api_data, safe_get, format_number, get_country_list
from components import render_comparison_summary_card
import pandas as pd
import plotly.graph_objects as go


def render():
    """Render the Climate Comparisons page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #c2410c;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-balance-scale"></i> Climate Comparisons</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Side-by-side comparison of two countries' climate
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get global parameters
    server_address = st.session_state.get('server_address', '152.53.160.43:8000')
    start_year = st.session_state.get('start_year', 1950)
    end_year = st.session_state.get('end_year', 2019)
    country_A = st.session_state.get('country_prefix', 'FR')
    
    # Country B selector on the page
    country_list = get_country_list()
    
    # Filter out country A from the list for country B selection
    country_B_options = [c for c in country_list if c != country_A]
    
    # Country B selector - small and above the comparison boxes
    col_spacer1, col_selector, col_spacer2 = st.columns([2, 2, 2])
    with col_selector:
        country_B = st.selectbox(
            "Select Country B",
            options=country_B_options,
            index=0,
            key="comparison_country_B"
        )
    
    # Display comparison in styled containers
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
            <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); 
                        border-radius: 10px; border: 2px solid #f97316;'>
                <div style='color: #7c2d12; font-size: 0.9rem; font-weight: 500;'>Country A</div>
                <div style='color: #7c2d12; font-size: 2.5rem; font-weight: 700;'>{country_A}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='display: flex; align-items: center; justify-content: center; height: 100%;'><span style='font-size: 2rem; color: #9ca3af;'>vs</span></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%); 
                        border-radius: 10px; border: 2px solid #3b82f6;'>
                <div style='color: #1e3a8a; font-size: 0.9rem; font-weight: 500;'>Country B</div>
                <div style='color: #1e3a8a; font-size: 2.5rem; font-weight: 700;'>{country_B}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Fetch data
    params = {
        'country_A_prefix': country_A,
        'country_B_prefix': country_B,
        'start_year': start_year,
        'end_year': end_year
    }
    
    data = fetch_api_data(server_address, 'comparisons', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/compare/?country_A={country_A}&country_B={country_B}&start_year={start_year}&end_year={end_year}")
        return
    
    # Summary row: 3 cards
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #f97316; padding-left: 1rem;'>
            <i class="fas fa-chart-bar"></i> Summary Comparison
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    country_A_summary = safe_get(data, 'country_A_summary', default={})
    country_B_summary = safe_get(data, 'country_B_summary', default={})
    difference = safe_get(data, 'difference', default={})
    
    with col1:
        # Country A Summary
        avg_temp_A = format_number(country_A_summary.get('avg_temp'), 2, "°C")
        
        temp_range_A = country_A_summary.get('temp_range', {})
        temp_range_str_A = f"{format_number(temp_range_A.get('start'), 1)}° to {format_number(temp_range_A.get('end'), 1)}°"
        
        total_precip_A = format_number(country_A_summary.get('total_precip'), 2, "mm")
        extreme_events_A = format_number(country_A_summary.get('extreme_events'), 0, "")
        
        render_comparison_summary_card(
            f"Country A ({country_A})",
            avg_temp_A,
            temp_range_str_A,
            total_precip_A,
            extreme_events_A,
            card_type='country_a'
        )
    
    with col2:
        # Difference
        avg_temp_diff = format_number(difference.get('avg_temp'), 2, "°C")
        total_precip_diff = format_number(difference.get('total_precip'), 2, "mm")
        extreme_events_diff = format_number(difference.get('extreme_events'), 0, "")
        
        render_comparison_summary_card(
            "Difference (A - B)",
            avg_temp_diff,
            None,  # No temp range for difference card
            total_precip_diff,
            extreme_events_diff,
            card_type='difference'
        )
    
    with col3:
        # Country B Summary
        avg_temp_B = format_number(country_B_summary.get('avg_temp'), 2, "°C")
        
        temp_range_B = country_B_summary.get('temp_range', {})
        temp_range_str_B = f"{format_number(temp_range_B.get('start'), 1)}° to {format_number(temp_range_B.get('end'), 1)}°"
        
        total_precip_B = format_number(country_B_summary.get('total_precip'), 2, "mm")
        extreme_events_B = format_number(country_B_summary.get('extreme_events'), 0, "")
        
        render_comparison_summary_card(
            f"Country B ({country_B})",
            avg_temp_B,
            temp_range_str_B,
            total_precip_B,
            extreme_events_B,
            card_type='country_b'
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Temperature comparison charts
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #ef4444; padding-left: 1rem;'>
            <i class="fas fa-temperature-high"></i> Temperature Comparisons
        </h3>
    """, unsafe_allow_html=True)
    
    data_point = safe_get(data, 'data_point', default={})
    
    # Maximum Temperature Comparison
    st.markdown("#### Maximum Temperature Over Time")
    
    with st.container(border=True):
        max_temp_A = data_point.get('max_temp_A', [])
        max_temp_B = data_point.get('max_temp_B', [])
        
        if max_temp_A and max_temp_B:
            # Create combined DataFrame
            df_A = pd.DataFrame(max_temp_A)
            df_B = pd.DataFrame(max_temp_B)
            
            if 'timestamp' in df_A.columns and 'timestamp' in df_B.columns:
                df_A = df_A.set_index('timestamp')
                df_B = df_B.set_index('timestamp')
                
                # Combine data
                combined_df = pd.DataFrame()
                
                if 'max_temp' in df_A.columns:
                    combined_df[f'{country_A} Max Temp (°C)'] = df_A['max_temp']
                
                if 'max_temp' in df_B.columns:
                    combined_df[f'{country_B} Max Temp (°C)'] = df_B['max_temp']
                
                if not combined_df.empty:
                    # Filter out sentinel values
                    combined_df = combined_df.replace([999.0, -999.0], float('nan'))
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    
                    # Add trace for country A
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df[f'{country_A} Max Temp (°C)'],
                        mode='lines',
                        name=f'{country_A} Max Temp',
                        line=dict(color='#f97316', width=3),
                        hovertemplate=f'{country_A}<br>Year: %{{x}}<br>Temp: %{{y}}°C<extra></extra>'
                    ))
                    
                    # Add trace for country B
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df[f'{country_B} Max Temp (°C)'],
                        mode='lines',
                        name=f'{country_B} Max Temp',
                        line=dict(color='#3b82f6', width=3),
                        hovertemplate=f'{country_B}<br>Year: %{{x}}<br>Temp: %{{y}}°C<extra></extra>'
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
                else:
                    st.warning("No valid temperature data to display")
            else:
                st.warning("Timestamp field not found in data")
        else:
            st.warning("Comparison temperature data not available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Minimum Temperature Comparison
    st.markdown("#### Minimum Temperature Over Time")
    
    with st.container(border=True):
        min_temp_A = data_point.get('min_temp_A', [])
        min_temp_B = data_point.get('min_temp_B', [])
        
        if min_temp_A and min_temp_B:
            # Create combined DataFrame
            df_A = pd.DataFrame(min_temp_A)
            df_B = pd.DataFrame(min_temp_B)
            
            if 'timestamp' in df_A.columns and 'timestamp' in df_B.columns:
                df_A = df_A.set_index('timestamp')
                df_B = df_B.set_index('timestamp')
                
                # Combine data
                combined_df = pd.DataFrame()
                
                if 'min_temp' in df_A.columns:
                    combined_df[f'{country_A} Min Temp (°C)'] = df_A['min_temp']
                
                if 'min_temp' in df_B.columns:
                    combined_df[f'{country_B} Min Temp (°C)'] = df_B['min_temp']
                
                if not combined_df.empty:
                    # Filter out sentinel values
                    combined_df = combined_df.replace([999.0, -999.0], float('nan'))
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    
                    # Add trace for country A
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df[f'{country_A} Min Temp (°C)'],
                        mode='lines',
                        name=f'{country_A} Min Temp',
                        line=dict(color='#f97316', width=3),
                        hovertemplate=f'{country_A}<br>Year: %{{x}}<br>Temp: %{{y}}°C<extra></extra>'
                    ))
                    
                    # Add trace for country B
                    fig.add_trace(go.Scatter(
                        x=combined_df.index,
                        y=combined_df[f'{country_B} Min Temp (°C)'],
                        mode='lines',
                        name=f'{country_B} Min Temp',
                        line=dict(color='#3b82f6', width=3),
                        hovertemplate=f'{country_B}<br>Year: %{{x}}<br>Temp: %{{y}}°C<extra></extra>'
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
                else:
                    st.warning("No valid temperature data to display")
            else:
                st.warning("Timestamp field not found in data")
        else:
            st.warning("Comparison temperature data not available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Total Precipitation Comparison
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #10b981; padding-left: 1rem;'>
            <i class="fas fa-tint"></i> Total Precipitation Comparison
        </h3>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        precip_A = data_point.get('total_precip_A', [])
        precip_B = data_point.get('total_precip_B', [])
        
        if precip_A and precip_B:
            # Create combined DataFrame
            df_A = pd.DataFrame(precip_A)
            df_B = pd.DataFrame(precip_B)
            
            if 'timestamp' in df_A.columns and 'timestamp' in df_B.columns:
                df_A = df_A.set_index('timestamp')
                df_B = df_B.set_index('timestamp')
                
                # Combine data
                combined_df = pd.DataFrame()
                
                if 'total_precip' in df_A.columns:
                    combined_df[f'{country_A}'] = df_A['total_precip']
                
                if 'total_precip' in df_B.columns:
                    combined_df[f'{country_B}'] = df_B['total_precip']
                
                if not combined_df.empty:
                    # Filter out sentinel values
                    combined_df = combined_df.replace([999.0, -999.0], float('nan'))
                    
                    # Create plotly figure for side-by-side bars
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=combined_df.index,
                        y=combined_df[country_A],
                        name=f'{country_A} Precipitation (mm)',
                        marker=dict(
                            color='#fb923c',
                            line=dict(color='#f97316', width=1.5)
                        ),
                        hovertemplate='<b>' + country_A + '</b><br>Year: %{x}<br>Precip: %{y} mm<extra></extra>'
                    ))
                    fig.add_trace(go.Bar(
                        x=combined_df.index,
                        y=combined_df[country_B],
                        name=f'{country_B} Precipitation (mm)',
                        marker=dict(
                            color='#60a5fa',
                            line=dict(color='#3b82f6', width=1.5)
                        ),
                        hovertemplate='<b>' + country_B + '</b><br>Year: %{x}<br>Precip: %{y} mm<extra></extra>'
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
                            x=1
                        ),
                        xaxis=dict(
                            title="Year",
                            showgrid=True,
                            gridcolor='rgba(16,185,129,0.1)'
                        ),
                        yaxis=dict(
                            title="Precipitation (mm)",
                            showgrid=True,
                            gridcolor='rgba(16,185,129,0.1)'
                        ),
                        plot_bgcolor='rgba(236,253,245,0.3)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No valid precipitation data to display")
            else:
                st.warning("Timestamp field not found in data")
        else:
            st.warning("Comparison precipitation data not available")
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

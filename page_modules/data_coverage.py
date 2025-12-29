"""
Data Coverage Page - Coverage analysis over time.
"""

import streamlit as st
from api import fetch_api_data, safe_get, format_number
from components import render_kpi_card
import pandas as pd
import plotly.graph_objects as go


def render():
    """Render the Data Coverage page."""
    
    # Page header with modern styling
    st.markdown("""
        <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; margin-bottom: 2rem; border: 2px solid #5a67d8;'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'><i class="fas fa-chart-bar"></i> Data Coverage Analysis</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Comprehensive coverage metrics and missing data patterns
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
    
    data = fetch_api_data(server_address, 'coverage', params)
    
    if data is None:
        if st.session_state.get('debug_mode', False):
            with st.expander("Debug: Show expected endpoint"):
                st.code(f"GET http://{server_address}/coverage/?country_prefix={country_prefix}&start_year={start_year}&end_year={end_year}")
        return
    
    # KPI row: 3 cards with enhanced styling
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; 
                   border-left: 4px solid #667eea; padding-left: 1rem;'>
            <i class="fas fa-bolt"></i> Coverage Summary
        </h3>
    """, unsafe_allow_html=True)
    
    coverage_summary = safe_get(data, 'coverage_summary', default={})
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        total_missing = coverage_summary.get('total_missing_days', 0)
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                        border-radius: 10px; border: 2px solid #f87171; box-shadow: 0 2px 8px rgba(248,113,113,0.2);'>
                <div style='color: #991b1b; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-exclamation-triangle"></i> TOTAL MISSING DAYS</div>
                <div style='color: #7f1d1d; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(total_missing, 0, "")), unsafe_allow_html=True)
    
    with col2:
        missing_pct = coverage_summary.get('missing_percentage', 0)
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        border-radius: 10px; border: 2px solid #fbbf24; box-shadow: 0 2px 8px rgba(251,191,36,0.2);'>
                <div style='color: #92400e; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-bolt"></i> MISSING PERCENTAGE</div>
                <div style='color: #78350f; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(missing_pct, 2, "%")), unsafe_allow_html=True)
    
    with col3:
        stations_count = coverage_summary.get('stations_count', 0)
        st.markdown("""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        border-radius: 10px; border: 2px solid #3b82f6; box-shadow: 0 2px 8px rgba(59,130,246,0.2);'>
                <div style='color: #1e3a8a; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'><i class="fas fa-map-marker-alt"></i> NUMBER OF STATIONS</div>
                <div style='color: #1e40af; font-size: 2rem; font-weight: 700;'>{}</div>
            </div>
        """.format(format_number(stations_count, 0, "")), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Coverage by station table
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #10b981; padding-left: 1rem;'>
            <i class="fas fa-map-marked-alt"></i> Data Coverage by Station
        </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .stDataFrame {
                border: 2px solid #10b981 !important;
                border-radius: 8px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        coverage_per_station = safe_get(data, 'coverage_per_station', default=[])
        
        if coverage_per_station:
            df = pd.DataFrame(coverage_per_station)
            
            # Rename columns for display
            column_mapping = {
                'station_id': 'Station ID',
                'coverage_percentage': 'Coverage (%)',
                'missing_days': 'Missing Days',
                'start_year': 'Start Year',
                'end_year': 'End Year'
            }
            
            display_df = df.rename(columns=column_mapping)
            
            # Format coverage percentage
            if 'Coverage (%)' in display_df.columns:
                display_df['Coverage (%)'] = display_df['Coverage (%)'].round(2)
            
            # Display as interactive table
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            
            # Summary stats with enhanced styling
            st.markdown("""
                <div style='margin: 1.5rem 0; border-top: 2px solid #e5e7eb; padding-top: 1.5rem;'></div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3, gap="large")
            
            with col1:
                avg_coverage = df['coverage_percentage'].mean()
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background: #f0fdf4; 
                                border-radius: 8px; border: 2px solid #86efac;'>
                        <div style='color: #166534; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-chart-bar"></i> AVERAGE COVERAGE</div>
                        <div style='color: #14532d; font-size: 1.75rem; font-weight: 700; margin-top: 0.5rem;'>{:.2f}%</div>
                    </div>
                """.format(avg_coverage), unsafe_allow_html=True)
            
            with col2:
                max_coverage = df['coverage_percentage'].max()
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background: #dbeafe; 
                                border-radius: 8px; border: 2px solid #60a5fa;'>
                        <div style='color: #1e40af; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-check"></i> BEST COVERAGE</div>
                        <div style='color: #1e3a8a; font-size: 1.75rem; font-weight: 700; margin-top: 0.5rem;'>{:.2f}%</div>
                    </div>
                """.format(max_coverage), unsafe_allow_html=True)
            
            with col3:
                min_coverage = df['coverage_percentage'].min()
                st.markdown("""
                    <div style='text-align: center; padding: 1rem; background: #fee2e2; 
                                border-radius: 8px; border: 2px solid #f87171;'>
                        <div style='color: #991b1b; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-times"></i> WORST COVERAGE</div>
                        <div style='color: #7f1d1d; font-size: 1.75rem; font-weight: 700; margin-top: 0.5rem;'>{:.2f}%</div>
                    </div>
                """.format(min_coverage), unsafe_allow_html=True)
        else:
            st.warning("No station coverage data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Coverage over time as bar chart
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #8b5cf6; padding-left: 1rem;'>
            <i class="fas fa-chart-line"></i> Missing Data Over Time
        </h3>
    """, unsafe_allow_html=True)
    
    coverage_per_year = safe_get(data, 'coverage_per_year', default=[])
    
    with st.container(border=True):
        if coverage_per_year:
            df = pd.DataFrame(coverage_per_year)
            
            if 'year' in df.columns:
                df = df.set_index('year')
                
                # Create plotly figure for side-by-side bars
                fig = go.Figure()
                
                if 'missing_temp' in df.columns:
                    fig.add_trace(go.Bar(
                        x=df.index,
                        y=df['missing_temp'],
                        name='<i class="fas fa-temperature-high"></i> Temperature',
                        marker=dict(
                            color='#ef4444',
                            line=dict(color='#dc2626', width=1.5)
                        ),
                        hovertemplate='<b>Temperature</b><br>Year: %{x}<br>Missing: %{y} days<extra></extra>'
                    ))
                
                if 'missing_precip' in df.columns:
                    fig.add_trace(go.Bar(
                        x=df.index,
                        y=df['missing_precip'],
                        name='<i class="fas fa-tint"></i> Precipitation',
                        marker=dict(
                            color='#10b981',
                            line=dict(color='#059669', width=1.5)
                        ),
                        hovertemplate='<b>Precipitation</b><br>Year: %{x}<br>Missing: %{y} days<extra></extra>'
                    ))
                
                if 'missing_snow' in df.columns:
                    fig.add_trace(go.Bar(
                        x=df.index,
                        y=df['missing_snow'],
                        name='<i class="fas fa-snowflake"></i> Snowfall',
                        marker=dict(
                            color='#8b5cf6',
                            line=dict(color='#7c3aed', width=1.5)
                        ),
                        hovertemplate='<b>Snowfall</b><br>Year: %{x}<br>Missing: %{y} days<extra></extra>'
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
                        bordercolor="#a78bfa",
                        borderwidth=2
                    ),
                    xaxis=dict(
                        title="Year",
                        showgrid=True,
                        gridcolor='rgba(139,92,246,0.1)',
                        linecolor='#a78bfa',
                        linewidth=2
                    ),
                    yaxis=dict(
                        title="Missing Days",
                        showgrid=True,
                        gridcolor='rgba(139,92,246,0.1)',
                        linecolor='#a78bfa',
                        linewidth=2
                    ),
                    plot_bgcolor='rgba(250,245,255,0.3)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12, color='#1e293b')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Year field not found in coverage data")
        else:
            st.info("Coverage per year data not available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Coverage statistics
    st.markdown("""
        <h3 style='color: #1e293b; font-weight: 600; margin-bottom: 1rem; margin-top: 2rem;
                   border-left: 4px solid #f59e0b; padding-left: 1rem;'>
            <i class="fas fa-chart-bar"></i> Missing Data Summary by Element
        </h3>
    """, unsafe_allow_html=True)
    
    if coverage_per_year:
        df = pd.DataFrame(coverage_per_year)
        
        # Calculate total missing data for each element
        total_missing = {}
        
        if 'missing_temp' in df.columns:
            total_missing['Temperature'] = df['missing_temp'].sum()
        
        if 'missing_precip' in df.columns:
            total_missing['Precipitation'] = df['missing_precip'].sum()
        
        if 'missing_snow' in df.columns:
            total_missing['Snowfall'] = df['missing_snow'].sum()
        
        if total_missing:
            # Show statistics with enhanced styling
            col1, col2, col3 = st.columns(3, gap="large")
            
            with col1:
                if 'Temperature' in total_missing:
                    st.markdown("""
                        <div style='text-align: center; padding: 1.5rem; 
                                    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); 
                                    border-radius: 10px; border: 2px solid #f87171; 
                                    box-shadow: 0 4px 6px rgba(248,113,113,0.15);'>
                            <div style='color: #991b1b; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-temperature-high"></i> TEMPERATURE MISSING</div>
                            <div style='color: #7f1d1d; font-size: 2rem; font-weight: 700; margin-top: 0.5rem;'>{:,}</div>
                            <div style='color: #991b1b; font-size: 0.875rem; margin-top: 0.25rem;'>days</div>
                        </div>
                    """.format(total_missing['Temperature']), unsafe_allow_html=True)
            
            with col2:
                if 'Precipitation' in total_missing:
                    st.markdown("""
                        <div style='text-align: center; padding: 1.5rem; 
                                    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                                    border-radius: 10px; border: 2px solid #10b981; 
                                    box-shadow: 0 4px 6px rgba(16,185,129,0.15);'>
                            <div style='color: #065f46; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-tint"></i> PRECIPITATION MISSING</div>
                            <div style='color: #064e3b; font-size: 2rem; font-weight: 700; margin-top: 0.5rem;'>{:,}</div>
                            <div style='color: #065f46; font-size: 0.875rem; margin-top: 0.25rem;'>days</div>
                        </div>
                    """.format(total_missing['Precipitation']), unsafe_allow_html=True)
            
            with col3:
                if 'Snowfall' in total_missing:
                    st.markdown("""
                        <div style='text-align: center; padding: 1.5rem; 
                                    background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); 
                                    border-radius: 10px; border: 2px solid #8b5cf6; 
                                    box-shadow: 0 4px 6px rgba(139,92,246,0.15);'>
                            <div style='color: #6b21a8; font-size: 0.875rem; font-weight: 600;'><i class="fas fa-snowflake"></i> SNOWFALL MISSING</div>
                            <div style='color: #581c87; font-size: 2rem; font-weight: 700; margin-top: 0.5rem;'>{:,}</div>
                            <div style='color: #6b21a8; font-size: 0.875rem; margin-top: 0.25rem;'>days</div>
                        </div>
                    """.format(total_missing['Snowfall']), unsafe_allow_html=True)
    
    # Debug expander
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: View raw API response"):
            st.json(data)

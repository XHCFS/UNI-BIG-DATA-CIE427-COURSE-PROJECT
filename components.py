"""
UI components for GHCN Climate Analytics Dashboard.
Provides reusable card and visualization components.
"""

import streamlit as st
from typing import Any, Optional, List, Dict
import pandas as pd


def render_kpi_card(title: str, value: str, helper_text: str = ""):
    """
    Render a KPI card with title, value, and optional helper text.
    
    Args:
        title: Card title
        value: Main value to display
        helper_text: Optional small text below value
    """
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        background-color: #fafafa;
        text-align: center;
        height: 100%;
    ">
        <div style="
            font-size: 0.875rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 500;
        ">{title}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: #1f1f1f;
            margin: 0.5rem 0;
        ">{value}</div>
        <div style="
            font-size: 0.75rem;
            color: #999;
        ">{helper_text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_card_container(title: str, content_func):
    """
    Render a card container with a title and content.
    
    Args:
        title: Card title
        content_func: Function to call to render content inside card
    """
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #1f1f1f;
        ">{title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        content_func()


def render_extreme_event_row(label: str, date: str, value: str, color_scheme: dict = None):
    """
    Render a row in the extremes section.
    
    Args:
        label: Event label (e.g., "Hottest Day")
        date: Date string
        value: Temperature or value string
        color_scheme: Dict with 'label_color', 'value_color' keys
    """
    if color_scheme is None:
        color_scheme = {
            'label_color': '#1f1f1f',
            'date_color': '#666',
            'value_color': '#1f1f1f'
        }
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<strong style='color: {color_scheme['label_color']};'>{label}</strong>", unsafe_allow_html=True)
        st.markdown(f"<small style='color: {color_scheme['date_color']};'>{date}</small>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: right; font-size: 1.5rem; font-weight: 700; color: {color_scheme['value_color']};'>{value}</div>", 
                   unsafe_allow_html=True)


def render_seasonal_card(season: str, avg_temp: float, temp_range: tuple, 
                        total_precip: float, avg_snow: float, color_scheme: dict = None):
    """
    Render a seasonal summary card.
    
    Args:
        season: Season name
        avg_temp: Average temperature
        temp_range: Tuple of (min, max) temperature
        total_precip: Total precipitation
        avg_snow: Average snow depth
        color_scheme: Dict with 'bg', 'border', 'text' keys for styling
    """
    from api import format_number
    
    # Default color scheme
    if color_scheme is None:
        color_scheme = {
            'bg': '#fafafa',
            'border': '#e0e0e0',
            'text': '#1f1f1f'
        }
    
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid {color_scheme['border']};
        background: {color_scheme['bg']};
        box-shadow: 0 2px 8px {color_scheme['shadow']};
    ">
        <div style="
            font-size: 1.125rem;
            font-weight: 700;
            color: {color_scheme['text']};
            margin-bottom: 1rem;
        ">{season}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {color_scheme['text']};
            margin-bottom: 1rem;
        ">{format_number(avg_temp, 1, "°C")}</div>
        <div style="font-size: 0.875rem; color: {color_scheme['text_secondary']}; margin-bottom: 0.25rem;">
            Range {format_number(temp_range[0], 1)}° - {format_number(temp_range[1], 1)}°
        </div>
        <div style="font-size: 0.875rem; color: {color_scheme['text_secondary']}; margin-bottom: 0.25rem;">
            Precipitation {format_number(total_precip, 1, "mm")}
        </div>
        <div style="font-size: 0.875rem; color: {color_scheme['text_secondary']};">
            Snow depth {format_number(avg_snow, 1, "cm")}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_event_kpi_card(title: str, count: int, last_date: str = "", color_scheme: dict = None):
    """
    Render an event KPI card with count and last occurrence.
    
    Args:
        title: Event type
        count: Total count
        last_date: Last occurrence date
        color_scheme: Dict with 'bg', 'border', 'text', 'text_secondary' keys
    """
    # Default color scheme
    if color_scheme is None:
        color_scheme = {
            'bg': 'linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%)',
            'border': '#e0e0e0',
            'text': '#1f1f1f',
            'text_secondary': '#666',
            'shadow': 'rgba(0,0,0,0.1)'
        }
    
    last_text = f"Last: {last_date}" if last_date else ""
    
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid {color_scheme['border']};
        background: {color_scheme['bg']};
        text-align: center;
        box-shadow: 0 2px 8px {color_scheme['shadow']};
    ">
        <div style="
            font-size: 0.875rem;
            color: {color_scheme['text']};
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">{title}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {color_scheme['text']};
            margin: 0.5rem 0;
        ">{count:,}</div>
        <div style="
            font-size: 0.75rem;
            color: {color_scheme['text_secondary']};
            font-weight: 500;
        ">{last_text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_card(title: str, temp_value: str, precip_value: str, snow_value: str, color_scheme: dict = None):
    """
    Render a statistical summary card.
    
    Args:
        title: Stat name
        temp_value: Temperature stat value
        precip_value: Precipitation stat value
        snow_value: Snow stat value
        color_scheme: Dict with 'bg', 'border', 'text' keys
    """
    if color_scheme is None:
        color_scheme = {
            'bg': 'linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%)',
            'border': '#e0e0e0',
            'text': '#1f1f1f',
            'text_secondary': '#666',
            'shadow': 'rgba(0,0,0,0.1)'
        }
    
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid {color_scheme['border']};
        background: {color_scheme['bg']};
        text-align: center;
        box-shadow: 0 2px 8px {color_scheme['shadow']};
    ">
        <div style="
            font-size: 0.875rem;
            color: {color_scheme['text']};
            margin-bottom: 1rem;
            font-weight: 700;
        ">{title}</div>
        <div style="font-size: 0.875rem; margin-bottom: 0.5rem; color: {color_scheme['text_secondary']};">
            <strong><i class="fas fa-temperature-high"></i> Temp:</strong> {temp_value}
        </div>
        <div style="font-size: 0.875rem; margin-bottom: 0.5rem; color: {color_scheme['text_secondary']};">
            <strong><i class="fas fa-tint"></i> Precip:</strong> {precip_value}
        </div>
        <div style="font-size: 0.875rem; color: {color_scheme['text_secondary']};">
            <strong><i class="fas fa-snowflake"></i> Snow:</strong> {snow_value}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_comparison_summary_card(title: str, avg_temp: str, temp_range: str, 
                                   total_precip: str, extreme_events: str, card_type: str = 'default'):
    """
    Render a country comparison summary card.
    
    Args:
        title: Card title
        avg_temp: Average temperature
        temp_range: Temperature range
        total_precip: Total precipitation
        extreme_events: Extreme events count
        card_type: 'country_a' (coral), 'difference' (purple), 'country_b' (blue), or 'default'
    """
    # Define color schemes
    color_schemes = {
        'country_a': {
            'gradient': 'linear-gradient(135deg, #fed7aa 0%, #fdba74 100%)',
            'border': '#f97316',
            'text': '#7c2d12'
        },
        'difference': {
            'gradient': 'linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%)',
            'border': '#a855f7',
            'text': '#581c87'
        },
        'country_b': {
            'gradient': 'linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%)',
            'border': '#3b82f6',
            'text': '#1e3a8a'
        },
        'default': {
            'gradient': '#fafafa',
            'border': '#e0e0e0',
            'text': '#1f1f1f'
        }
    }
    
    colors = color_schemes.get(card_type, color_schemes['default'])
    
    # Build temp range row only if provided
    temp_range_row = ""
    if temp_range is not None:
        temp_range_row = f'<div style="font-size: 0.95rem; margin-bottom: 0.5rem; color: {colors["text"]};"><strong>Temp Range:</strong> {temp_range}</div>'
    
    st.markdown(
        f'<div style="padding: 1.5rem; border-radius: 12px; border: 2px solid {colors["border"]}; background: {colors["gradient"]}; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
        f'<div style="font-size: 1.2rem; font-weight: 700; color: {colors["text"]}; margin-bottom: 1rem; border-bottom: 2px solid {colors["border"]}; padding-bottom: 0.5rem;">{title}</div>'
        f'<div style="font-size: 0.95rem; margin-bottom: 0.5rem; color: {colors["text"]};"><strong>Avg Temp:</strong> {avg_temp}</div>'
        f'{temp_range_row}'
        f'<div style="font-size: 0.95rem; margin-bottom: 0.5rem; color: {colors["text"]};"><strong>Total Precip:</strong> {total_precip}</div>'
        f'<div style="font-size: 0.95rem; color: {colors["text"]};"><strong>Extreme Events:</strong> {extreme_events}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def create_line_chart_data(data_points: List[Dict], x_field: str, y_fields: List[str]) -> pd.DataFrame:
    """
    Create a DataFrame for line chart from API data points.
    
    Args:
        data_points: List of data point dictionaries
        x_field: Field name for x-axis (usually timestamp/year)
        y_fields: List of field names for y-axis values
    
    Returns:
        DataFrame suitable for st.line_chart
    """
    if not data_points:
        return pd.DataFrame()
    
    df = pd.DataFrame(data_points)
    if x_field in df.columns:
        df = df.set_index(x_field)
    
    # Keep only requested fields
    available_fields = [f for f in y_fields if f in df.columns]
    if available_fields:
        return df[available_fields]
    return pd.DataFrame()


def create_bar_chart_data(data_points: List[Dict], x_field: str, y_field: str) -> pd.DataFrame:
    """
    Create a DataFrame for bar chart from API data points.
    
    Args:
        data_points: List of data point dictionaries
        x_field: Field name for x-axis
        y_field: Field name for y-axis
    
    Returns:
        DataFrame suitable for st.bar_chart
    """
    if not data_points:
        return pd.DataFrame()
    
    df = pd.DataFrame(data_points)
    if x_field in df.columns:
        df = df.set_index(x_field)
    
    if y_field in df.columns:
        return df[[y_field]]
    return pd.DataFrame()

"""
GHCN Climate Analytics Dashboard - Main Application
Multi-page Streamlit dashboard for climate data analysis.
"""

import streamlit as st
from api import get_country_list

# Page configuration
st.set_page_config(
    page_title="GHCN Climate Analytics",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add Font Awesome CSS
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Import page modules
import page_modules.overview as overview
import page_modules.geospatial_map as geospatial_map
import page_modules.trends as trends
import page_modules.seasonal_patterns as seasonal_patterns
import page_modules.extreme_events as extreme_events
import page_modules.statistical_analysis as statistical_analysis
import page_modules.comparisons as comparisons
import page_modules.data_coverage as data_coverage


def render_sidebar():
    """Render the sidebar with branding, controls, and navigation."""
    with st.sidebar:
        # Enhanced Branding with gradient
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
            <div style="
                font-size: 2.8rem;
                font-weight: 800;
                color: white;
                letter-spacing: 0.15em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            "><i class="fas fa-temperature-high"></i> GHCN</div>
            <div style="
                font-size: 1.1rem;
                color: rgba(255,255,255,0.95);
                margin-top: 0.5rem;
                font-weight: 500;
                letter-spacing: 0.05em;
            ">Climate Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration Section with styled header
        st.markdown("""
        <div style="
            margin: 1.5rem 0 1rem 0;
            padding: 0.5rem 0 0.5rem 1rem;
            border-left: 4px solid #667eea;
            background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
        ">
            <h3 style="margin: 0; color: #4c51bf; font-size: 1.1rem;"><i class="fas fa-cog"></i> Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Debug mode toggle with custom styling
        st.markdown("""
        <style>
            .stCheckbox > label {
                font-weight: 500;
                color: #4a5568;
            }
        </style>
        """, unsafe_allow_html=True)
        
        debug_mode = st.checkbox(
            "Debug Mode",
            value=False,
            help="Show debug information and raw API responses"
        )
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # Server address
        server_address = st.text_input(
            "Server Address",
            value="0.0.0.0:8000",
            help="API server address (without http://)"
        )
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # Year range with better spacing
        st.markdown("<div style='color: #4a5568; font-weight: 500; margin-bottom: 0.5rem;'><i class='far fa-calendar-alt'></i> Time Period</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input(
                "Start Year",
                min_value=1700,
                max_value=2100,
                value=1950,
                step=1
            )
        with col2:
            end_year = st.number_input(
                "End Year",
                min_value=1700,
                max_value=2100,
                value=2019,
                step=1
            )
        
        # Country selection (depends on page)
        country_list = get_country_list()
        
        # Check which page we're on for country selection
        page = st.session_state.get('page', 'Overview')
        
        # Country Selection Section with styled header
        st.markdown("""
        <div style="
            margin: 1.5rem 0 1rem 0;
            padding: 0.5rem 0 0.5rem 1rem;
            border-left: 4px solid #48bb78;
            background: linear-gradient(90deg, rgba(72, 187, 120, 0.1) 0%, transparent 100%);
        ">
            <h3 style="margin: 0; color: #2f855a; font-size: 1.1rem;"><i class="fas fa-globe"></i> Country Selection</h3>
        </div>
        """, unsafe_allow_html=True)
        
        country_prefix = st.selectbox(
            "Country",
            options=country_list,
            index=country_list.index("FR") if "FR" in country_list else 0,
            key="country_prefix"
        )
        
        # Navigation Section with styled header
        st.markdown("""
        <div style="
            margin: 1.5rem 0 1rem 0;
            padding: 0.5rem 0 0.5rem 1rem;
            border-left: 4px solid #f59e0b;
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%);
        ">
            <h3 style="margin: 0; color: #d97706; font-size: 1.1rem;"><i class="fas fa-compass"></i> Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Custom CSS for prettier radio buttons
        st.markdown("""
        <style>
            /* Radio button container */
            div[data-testid="stRadio"] > div {
                gap: 0.5rem;
            }
            
            /* Radio button labels */
            div[data-testid="stRadio"] label {
                background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 0.75rem 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                margin: 0.25rem 0;
            }
            
            /* Radio button hover effect */
            div[data-testid="stRadio"] label:hover {
                background: linear-gradient(135deg, rgba(56,189,248,0.15) 0%, rgba(59,130,246,0.1) 100%);
                border-color: rgba(56,189,248,0.4);
                transform: translateX(5px);
                box-shadow: 0 4px 12px rgba(56,189,248,0.2);
            }
            
            /* Selected radio button */
            div[data-testid="stRadio"] label:has(input:checked) {
                background: linear-gradient(135deg, rgba(56,189,248,0.25) 0%, rgba(59,130,246,0.2) 100%);
                border-color: rgba(56,189,248,0.6);
                box-shadow: 0 4px 16px rgba(56,189,248,0.3);
                font-weight: 600;
            }
            
            /* Hide the actual radio button circle */
            div[data-testid="stRadio"] input[type="radio"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
        
        pages = [
            "Overview",
            "Geospatial Map",
            "Trends & Time Series",
            "Seasonal Patterns",
            "Extreme Events",
            "Statistical Analysis",
            "Comparisons",
            "Data Coverage"
        ]
        
        selected_page = st.radio(
            "Select Page",
            pages,
            key='page_radio',
            label_visibility="collapsed"
        )
        
        # Footer with version info
        st.markdown("""
        <div style="
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #a0aec0;
            font-size: 0.75rem;
        ">
            <div style="margin-bottom: 0.25rem;">GHCN Dashboard v1.0</div>
            <div>Powered by Streamlit</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Store in session state
        st.session_state['page'] = selected_page
        st.session_state['debug_mode'] = debug_mode
        st.session_state['server_address'] = server_address
        st.session_state['start_year'] = start_year
        st.session_state['end_year'] = end_year
        
        return selected_page


def main():
    """Main application entry point."""
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Overview'
    
    # Render sidebar and get selected page
    current_page = render_sidebar()
    
    # Route to selected page
    if current_page == "Overview":
        overview.render()
    elif current_page == "Geospatial Map":
        geospatial_map.render()
    elif current_page == "Trends & Time Series":
        trends.render()
    elif current_page == "Seasonal Patterns":
        seasonal_patterns.render()
    elif current_page == "Extreme Events":
        extreme_events.render()
    elif current_page == "Statistical Analysis":
        statistical_analysis.render()
    elif current_page == "Comparisons":
        comparisons.render()
    elif current_page == "Data Coverage":
        data_coverage.render()


if __name__ == "__main__":
    main()

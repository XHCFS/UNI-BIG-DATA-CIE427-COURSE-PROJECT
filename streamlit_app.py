import streamlit as st
import requests
import pandas as pd
from typing import Optional

# This file acts as the application launcher.
# It sets the page configuration for the whole app.

st.set_page_config(
    page_title="Big Data Climate Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    # 🌎 Big Data Climate Analysis Dashboard
    
    Welcome! Please use the navigation menu on the left to explore the different
    sections of the analysis, starting with the **Overview** page.
    """
)


# --- Configuration ---
API_BASE_URL = "http://152.53.160.43:8000"
API_QUERY_PATH = "/api/run_query" # <--- **CHECK THIS PATH WITH YOUR TEAMMATE**
API_ENDPOINT = API_BASE_URL + API_QUERY_PATH
# ---------------------

@st.cache_data(ttl=300) # Cache test result for 5 minutes
def test_api_connection(url: str) -> bool:
    """Tests if the API is reachable using the simple /test endpoint."""
    test_url = url.replace(API_QUERY_PATH, "/test")
    try:
        response = requests.get(test_url, timeout=5)
        # Check for status 200 and the exact expected response body "HI :>"
        if response.status_code == 200 and response.text.strip().replace('"', '') == "HI :>":
            return True
        else:
            st.error(f"Test failed. API returned: HTTP {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API at {test_url}. Error: {e}")
        return False

# Test API connection first
if test_api_connection(API_ENDPOINT):
    st.success("Server Connection Verified: The API is up and running.")
    st.markdown("The connection to the server's `/test` endpoint is successful.")
else:
    st.error("Critical Error: Cannot connect to the API server. Please check the network, IP, and port.")
    st.stop() # Stop execution if the API is not available

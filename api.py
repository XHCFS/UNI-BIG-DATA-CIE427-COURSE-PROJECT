"""
API helper module for GHCN Climate Analytics Dashboard.
Handles URL construction, JSON fetching, and caching.
"""

import json
import urllib.request
import urllib.parse
import streamlit as st
from typing import Dict, Any, Optional


def build_url(server_address: str, path: str, params: Dict[str, Any]) -> str:
    """
    Build a complete URL with query parameters.
    
    Args:
        server_address: Base server address (e.g., "152.53.160.43:8000")
        path: API path (e.g., "overview")
        params: Dictionary of query parameters
    
    Returns:
        Complete URL string
    """
    # Remove leading/trailing slashes from path
    path = path.strip('/')
    
    # Filter out None values from params
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    # Build query string
    query_string = urllib.parse.urlencode(filtered_params)
    
    # Construct full URL
    url = f"http://{server_address}/{path}/?{query_string}"
    return url


@st.cache_data(ttl=300)
def fetch_json(url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch JSON data from a URL with caching.
    
    Args:
        url: Complete URL to fetch
    
    Returns:
        Parsed JSON as dictionary, or None on error
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            return json.loads(data)
    except Exception as e:
        return None


def fetch_api_data(server_address: str, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Fetch data from API endpoint with error handling and loading UI.
    
    Args:
        server_address: Base server address
        endpoint: API endpoint path
        params: Query parameters
    
    Returns:
        Parsed JSON response or None on error
    """
    url = build_url(server_address, endpoint, params)
    
    with st.spinner(f"Loading data from {endpoint}..."):
        data = fetch_json(url)
    
    if data is None:
        st.error(f"Failed to fetch data from: {url}")
        st.error("Please check the server address and parameters.")
        return None
    
    return data


def safe_get(data: Dict, *keys, default=None):
    """
    Safely get nested dictionary values.
    
    Args:
        data: Dictionary to query
        *keys: Sequence of keys to traverse
        default: Default value if path doesn't exist
    
    Returns:
        Value at the specified path or default
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def format_number(value: Any, decimals: int = 2, unit: str = "") -> str:
    """
    Format a numeric value with proper handling of None/invalid values.
    
    Args:
        value: Value to format
        decimals: Number of decimal places
        unit: Optional unit suffix
    
    Returns:
        Formatted string
    """
    if value is None:
        return "--"
    
    try:
        num = float(value)
        if num == 999.0 or num == -999.0:  # Handle sentinel values
            return "--"
        formatted = f"{num:,.{decimals}f}"
        return f"{formatted} {unit}".strip()
    except (ValueError, TypeError):
        return "--"


# Common country prefixes (fallback if file not available)
DEFAULT_COUNTRY_PREFIXES = [
    "AC", "AE", "AF", "AG", "AJ", "AL", "AM", "AO", "AQ", "AR", "AS", "AU", "AY",
    "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BK", "BL", "BM", "BN", "BO",
    "BP", "BR", "BU", "BX", "BY", "CA", "CB", "CD", "CE", "CF", "CG", "CH", "CI",
    "CJ", "CK", "CM", "CO", "CQ", "CS", "CT", "CU", "CV", "CW", "CY", "DA", "DO",
    "DR", "EC", "EG", "EI", "EK", "EN", "ER", "ES", "ET", "EU", "EZ", "FG", "FI",
    "FJ", "FK", "FM", "FP", "FR", "FS", "GA", "GB", "GG", "GH", "GI", "GL", "GM",
    "GP", "GQ", "GR", "GT", "GV", "GY", "HO", "HR", "HU", "IC", "ID", "IN", "IO",
    "IR", "IS", "IT", "IV", "IZ", "JA", "JM", "JN", "JO", "JQ", "JU", "KE", "KG",
    "KN", "KR", "KS", "KT", "KU", "KZ", "LA", "LE", "LG", "LH", "LI", "LO", "LQ",
    "LT", "LU", "LY", "MA", "MB", "MC", "MD", "MF", "MG", "MI", "MJ", "MK", "ML",
    "MO", "MP", "MQ", "MR", "MT", "MU", "MV", "MX", "MY", "MZ", "NC", "NE", "NF",
    "NG", "NH", "NI", "NL", "NN", "NO", "NP", "NS", "NU", "NZ", "PA", "PC", "PE",
    "PK", "PL", "PM", "PO", "PP", "PS", "PU", "QA", "RE", "RI", "RM", "RO", "RP",
    "RQ", "RS", "RW", "SA", "SB", "SE", "SF", "SG", "SH", "SI", "SL", "SN", "SP",
    "ST", "SU", "SV", "SW", "SX", "SY", "SZ", "TD", "TE", "TH", "TI", "TL", "TN",
    "TO", "TS", "TU", "TV", "TX", "TZ", "UC", "UG", "UK", "UP", "US", "UV", "UY",
    "UZ", "VE", "VM", "VQ", "WA", "WF", "WI", "WQ", "WZ", "ZA", "ZI"
]


def get_country_list() -> list:
    """
    Get list of country prefixes.
    Try to load from ghcnd_countries file, fallback to default list.
    
    Returns:
        List of country prefix codes
    """
    # TODO: Implement file loading if ghcnd_countries file is available
    # For now, return default list
    return sorted(DEFAULT_COUNTRY_PREFIXES)

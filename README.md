# GHCN Climate Analytics Dashboard

A climatology report dashboard optimized using Hadoop and built with Streamlit. This multi-page interactive dashboard provides comprehensive climate data analysis including trends, seasonal patterns, extreme events, and geospatial visualizations.

## Features

- **Overview**: Key climate metrics and summaries
- **Geospatial Map**: Interactive maps showing climate data distribution
- **Trends Analysis**: Long-term climate trends and patterns
- **Seasonal Patterns**: Seasonal variations in climate data
- **Extreme Events**: Analysis of extreme weather events
- **Statistical Analysis**: Detailed statistical insights
- **Comparisons**: Compare climate data across regions
- **Data Coverage**: Data availability and coverage information

## Prerequisites

- Python 3.8 or higher
- Backend API server running (default: `152.53.160.43:8000`)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd UNI-BIG-DATA-CIE427-COURSE-PROJECT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit dashboard:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Configuration

The dashboard connects to a backend API server. You can configure the server address in the sidebar settings within the application.

Default server: `152.53.160.43:8000`

## Dependencies

- `streamlit>=1.28.0` - Web application framework
- `pandas>=2.0.0` - Data manipulation and analysis
- `plotly>=5.0.0` - Interactive charts and visualizations
- `pydeck>=0.8.0` - Geospatial map rendering

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── api.py              # API helper functions
├── components.py       # Reusable UI components
├── requirements.txt    # Python dependencies
├── page_modules/       # Dashboard page modules
│   ├── overview.py
│   ├── geospatial_map.py
│   ├── trends.py
│   ├── seasonal_patterns.py
│   ├── extreme_events.py
│   ├── statistical_analysis.py
│   ├── comparisons.py
│   └── data_coverage.py
└── README.md
```

## License

See [LICENSE](LICENSE) file for details.

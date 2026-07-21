# Daily Located ET0

Live demo: https://daily-evapotranspiration.streamlit.app/

A small Streamlit app that fetches hourly weather from Open-Meteo and calculates/display daily FAO evapotranspiration (ET0) for a specific location. Enter a place name or coordinates and see hourly ET0 and precipitation summarized for the day.

## Features
- Locate a position using Nominatim (geopy)
- Fetch hourly ET0 and precipitation from Open-Meteo
- Cache API responses to reduce repeated requests
- Display hourly data and daily totals in a Streamlit table and badges
- Simple, single-file Streamlit app (main.py)

## Demo
Open the live demo: https://daily-evapotranspiration.streamlit.app/

(If the link goes down, run locally — instructions below.)

## Installation
1. Clone the repository
   git clone https://github.com/Griffith0110/ET0.git
   cd ET0
2. Create and activate a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows
3. Install dependencies
   pip install -r requirements.txt

## Run locally
Start the Streamlit app:
streamlit run main.py

## Configuration & Notes
- No API key is required for Open-Meteo.
- The app uses Nominatim (geopy) for converting place names into coordinates. Please respect the Nominatim usage policy:
  - Use a unique user_agent (the code uses "ET0").
  - Avoid heavy automated querying; use caching to reduce repeated geocoding calls.
- The app uses requests_cache to cache API responses in the `.cache` file for 1 hour (see main.py).

## Dependencies
See requirements.txt:
- streamlit
- openmeteo_requests
- geopy
- pandas
- requests_cache
- retry_requests

## How it works
- Geocode user input with Nominatim to get lat/lon.
- Query Open-Meteo hourly forecast for ET0 and precipitation.
- Build a pandas DataFrame with hourly timestamps and values.
- Display results and daily totals in Streamlit.

## Troubleshooting
- If geocoding fails, try more specific location names (city, state, country) or use coordinates (lat, lon).
- If the Open-Meteo response changes format, verify the requested hourly variable names match the API response.
- If Streamlit shows Unicode/timezone warnings, confirm the system timezone and Pandas versions.

## Acknowledgements
- Data provided by https://open-meteo.com (CC BY 4.0)
- Geocoding via Nominatim / OpenStreetMap

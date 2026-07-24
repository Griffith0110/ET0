import openmeteo_requests
import geopy
import pandas as pd
import requests_cache
from retry_requests import retry
import streamlit as st

geolocator = geopy.geocoders.Nominatim(user_agent="ET0 ")
location = geolocator.geocode(st.chat_input("Position"))


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    f"latitude": {location.latitude},
    f"longitude": {location.longitude},
    "daily": [
        "et0_fao_evapotranspiration",
        "precipitation_sum",
    ],
    "models":"italia_meteo_arpae_icon_2i",
    "timezone": "auto",
    "forecast_days": 1,
    "past_day": 1,
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
st.subheader("ET0")
st.text(f"📍 {location.address}",text_alignment="justify")
st.badge(f"🧭 {response.Latitude()}°N\t{response.Longitude()}°E", color="green")
st.badge(f"⛰️ {response.Elevation()} m slm", color="yellow")

# Process hourly data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_et0_fao_evapotranspiration = daily.Variables(0).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()

daily_data = {
    "📅": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    ).tz_convert(response.Timezone().decode())
}
daily_data["🌿 ET0 (FAO) mm/m² "] = daily_et0_fao_evapotranspiration
daily_data["🌧️ mm/m² "] = daily_precipitation_sum
daily_dataframe = pd.DataFrame(data=daily_data)
st.dataframe(daily_dataframe,hide_index=True)
st.badge("Data provided by https://open-meteo.com - © 2022–2026 Open-Meteo (CC BY 4.0)")

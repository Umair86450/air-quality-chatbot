import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from groq import Groq

# Groq API setup
client = Groq(api_key="Your groq api key")

# OpenWeather API setup
OPENWEATHER_API_KEY = "your weather api key"
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# AQI Categories
AQI_CATEGORIES = {
    1: "Good (0-50)",
    2: "Moderate (51-100)",
    3: "Unhealthy for Sensitive Groups (101-150)",
    4: "Unhealthy (151-200)",
    5: "Very Unhealthy (201-300)"
}

# --- Streamlit Frontend ---
st.title("🌍 Air Quality Chatbot")
st.subheader("Your Personalized AI Assistant for Air Pollution")

# Sidebar User Input Section
st.sidebar.title("User Details")
location = st.sidebar.text_input("Enter your location (City Name):", "Pakistan")

# Health conditions in a dropdown
health_condition = st.sidebar.selectbox(
    "Do you have any of these conditions?",
    [
        "None",
        "Asthma",
        "Chronic Obstructive Pulmonary Disease (COPD)",
        "Lung Cancer",
        "Heart Disease",
        "Hypertension (High Blood Pressure)",
        "Cognitive Decline",
        "Pregnancy (Low Birth Weight Risk)"
    ]
)

# Function to get latitude and longitude of a location
def get_location_coordinates(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(geo_url).json()
        if response:
            return response[0]['lat'], response[0]['lon']
    except Exception:
        st.error("Error fetching location data. Please check the city name.")
    return None, None

# Function to fetch air quality data
def get_air_quality(lat, lon):
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        }
        response = requests.get(OPENWEATHER_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception:
        st.error("Error fetching air quality data. Please try again later.")
    return None

# Function to call Groq API for personalized advice
def get_personalized_advice(health_condition, aqi, components):
    pollutants = f"""
    - PM2.5: {components['pm2_5']} µg/m³
    - PM10: {components['pm10']} µg/m³
    - NO2: {components['no2']} µg/m³
    - CO: {components['co']} µg/m³
    """
    query = f"""
    You are an air quality and health advisor. The user has the condition: '{health_condition}'.
    The air quality index (AQI) is {aqi}, categorized as '{categorize_aqi(aqi)}'.
    Pollutant levels are:
    {pollutants}
    
    Based on this information, provide:
    1. Specific health precautions for the user.
    2. Recommended indoor and outdoor activities.
    3. Additional lifestyle tips to mitigate air pollution effects.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Unable to fetch advice at the moment. Please try again later."

# Function to categorize AQI
def categorize_aqi(aqi):
    return AQI_CATEGORIES.get(aqi, "Unknown")

# Function to visualize real-time pollutant data
def visualize_realtime_pollutants(components):
    pollutants = {
        "Carbon Monoxide (CO)": components['co'],
        "Nitrogen Dioxide (NO2)": components['no2'],
        "Fine Particulate Matter (PM2.5)": components['pm2_5'],
        "Coarse Particulate Matter (PM10)": components['pm10'],
    }
    df = pd.DataFrame(list(pollutants.items()), columns=['Pollutant', 'Concentration (µg/m³)'])
    fig = px.bar(df, x='Pollutant', y='Concentration (µg/m³)', title="Pollutant Levels", text='Concentration (µg/m³)')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(title_font_size=20, title_x=0.5)
    st.plotly_chart(fig)

# Chatbot Functionality
def chatbot_response(user_input):
    prompt = f"""
    You are an air quality expert. A user asked: "{user_input}".
    Provide a clear, actionable, and accurate response regarding their question on air pollution and its health effects.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Unable to process your query at the moment. Please try again later."

# Main Application Logic
if location:
    lat, lon = get_location_coordinates(location)
    if lat and lon:
        air_quality_data = get_air_quality(lat, lon)
        if air_quality_data:
            aqi = air_quality_data['list'][0]['main']['aqi']
            components = air_quality_data['list'][0]['components']
            category = categorize_aqi(aqi)
            
            # Display AQI Information
            st.metric(label="Current AQI", value=category)
            st.write(f"PM10 Levels: {components['pm10']} µg/m³")
            st.write(f"PM2.5 Levels: {components['pm2_5']} µg/m³")
            
            # Real-Time Visualization
            st.subheader("Real-Time Pollution Trends")
            visualize_realtime_pollutants(components)
            
            # Call Groq API for personalized advice
            st.subheader("Personalized Health Advice")
            advice = get_personalized_advice(health_condition, aqi, components)
            st.write(advice)
            
            # Chatbot Section
            st.subheader("Chat with the Air Quality Bot")
            user_query = st.text_input("Ask a question about air pollution or health:")
            if user_query:
                bot_response = chatbot_response(user_query)
                st.write(bot_response)
        else:
            st.error("Unable to fetch air quality data.")
    else:
        st.error("Unable to fetch location coordinates.")

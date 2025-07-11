# 🌍 AirCare AI - Air Quality Chatbot

**AirCare AI** is a smart Streamlit-based web application that monitors real-time air quality and provides **personalized health advice** using **AI-powered chat**. It helps users understand pollution levels in their area and get tailored health precautions—especially useful for people with sensitive health conditions.

---

## 🚀 Features

- 🌫️ **Real-time AQI (Air Quality Index)** using OpenWeatherMap
- 📈 **Pollutant Level Visualization** (PM2.5, PM10, NO2, CO)
- 💬 **AI Chatbot** to answer health-related pollution queries
- 🩺 **Personalized Advice** based on user's health condition
- 🗺️ **Geolocation** support using city name
- 📊 Interactive charts with Plotly

---

## 🛠️ Tech Stack

| Technology     | Purpose                          |
|----------------|----------------------------------|
| Streamlit      | Frontend web UI                  |
| Groq LLM       | AI chatbot and health advice     |
| OpenWeatherMap | Real-time air quality data       |
| Plotly         | Interactive pollutant bar charts |
| Pandas         | Data formatting for charts       |
| Requests       | API data fetching                |

---

## 🔑 Required APIs & Setup

To run this project, you **must provide valid API keys** for:

### 1. 🧠 **Groq API** (For AI-powered chatbot & advice)
- Sign up at: [https://console.groq.com](https://console.groq.com)
- Create an API key
- Replace this line in the code:
  ```python
  client = Groq(api_key="Your groq api key")
````
Yahan aapke diye gaye Markdown section ka **accurately structured and properly formatted version** hai. Maine indentation, headings aur spacing ko clean aur consistent bana diya hai:

---

````markdown
### 2. 🌦️ OpenWeatherMap API (For AQI data and coordinates)

- Sign up at: [https://openweathermap.org/api](https://openweathermap.org/api)
- Get your API key and replace the following line in the code:

  ```python
  OPENWEATHER_API_KEY = "your weather api key"
````

---

## 📦 Installation

### ✅ Prerequisites

* Python 3.10+
* Virtual environment (optional but recommended)

### 📥 Clone the repository

```bash
git clone https://github.com/your-username/aircare-ai.git
cd aircare-ai
```

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the app

```bash
streamlit run app.py
```

---

## 👤 User Inputs

* **City name** for AQI
* **Health condition** from dropdown (e.g., Asthma, COPD)
* **User questions** via chatbot

---

## ❗ Important Notes

* If you don't provide valid **Groq** and **OpenWeatherMap** API keys, the app **will not function properly**.
* All API calls depend on correct input (e.g., valid city names).

---

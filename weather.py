import requests
import folium
from gtts import gTTS
from IPython.display import display, Audio

# ----------------------------
# Text To Speech
# ----------------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("weather.mp3")
    display(Audio("weather.mp3", autoplay=True))

city = input("Enter any city in the world: ")

# ----------------------------
# Get Latitude & Longitude
# ----------------------------
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

geo = requests.get(geo_url).json()

if "results" not in geo:
    print("City not found!")
else:

    place = geo["results"][0]

    lat = place["latitude"]
    lon = place["longitude"]
    country = place["country"]

    # ----------------------------
    # Weather
    # ----------------------------

    weather_url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&timezone=auto"
    )

    weather = requests.get(weather_url).json()

    current = weather["current"]

    print("\nCurrent Weather")
    print("-------------------------")
    print("City:", city.title())
    print("Country:", country)
    print("Temperature:", current["temperature_2m"], "°C")
    print("Humidity:", current["relative_humidity_2m"], "%")
    print("Wind Speed:", current["wind_speed_10m"], "km/h")

    print("\n7-Day Forecast")
    print("-------------------------")

    daily = weather["daily"]

    for i in range(7):
        print(
            daily["time"][i],
            "| High:", daily["temperature_2m_max"][i],
            "| Low:", daily["temperature_2m_min"][i],
            "| Rain:", daily["precipitation_probability_max"][i], "%"
        )

    # ----------------------------
    # Interactive Map
    # ----------------------------

    m = folium.Map(location=[lat, lon], zoom_start=10)

    folium.Marker(
        [lat, lon],
        popup=f"{city.title()}, {country}",
        tooltip=city.title()
    ).add_to(m)

    display(m)

    # ----------------------------
    # Voice Assistant
    # ----------------------------

    speech = f"""
    The current temperature in {city} is {current['temperature_2m']} degrees Celsius.
    Humidity is {current['relative_humidity_2m']} percent.
    Wind speed is {current['wind_speed_10m']} kilometers per hour.
    The highest chance of rain today is {daily['precipitation_probability_max'][0]} percent.
    """

    speak(speech)

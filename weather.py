import requests
import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display, Javascript
from google.colab import output
from base64 import b64decode
from pydub import AudioSegment
import folium

# -------------------- Record Voice --------------------
def record():
    print("🎤 Speak now (Example: 'What is the weather in Tokyo?')")
    js = Javascript("""
    async function record(){
      const stream = await navigator.mediaDevices.getUserMedia({audio:true});
      const recorder = new MediaRecorder(stream);
      let chunks = [];
      recorder.ondataavailable = e => chunks.push(e.data);
      recorder.start();
      await new Promise(r => setTimeout(r,5000));
      recorder.stop();
      await new Promise(r => recorder.onstop = r);
      const blob = new Blob(chunks);
      const reader = new FileReader();
      reader.readAsDataURL(blob);
      await new Promise(r => reader.onloadend = r);
      return reader.result;
    }
    record();
    """)
    data = output.eval_js(js)
    binary = b64decode(data.split(",")[1])

    with open("voice.webm","wb") as f:
        f.write(binary)

    AudioSegment.from_file("voice.webm").export("voice.wav",format="wav")

    r = sr.Recognizer()

    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)

    return r.recognize_google(audio)

# -------------------- Speak --------------------
def speak(text):
    tts = gTTS(text=text)
    tts.save("weather.mp3")
    display(Audio("weather.mp3", autoplay=True))

# -------------------- Voice Input --------------------
try:
    sentence = record()
except:
    sentence = input("Couldn't hear you. Type the city name instead: ")

print("\nYou said:", sentence)

city = sentence.lower()
city = city.replace("what is the weather in","")
city = city.replace("weather in","")
city = city.replace("tell me the weather in","")
city = city.replace("?","").strip()

# -------------------- Geocoding --------------------
geo = requests.get(
    f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
).json()

if "results" not in geo:
    print("❌ City not found.")
else:

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    country = geo["results"][0]["country"]

    # -------------------- Weather --------------------
    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&timezone=auto"
    ).json()

    current = weather["current"]
    daily = weather["daily"]

    temp_c = current["temperature_2m"]
    temp_f = round((temp_c * 9/5) + 32, 1)

    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    rain = daily["precipitation_probability_max"][0]

    # -------------------- AI Advice --------------------
    advice = ""

    if temp_c >= 35:
        advice += "It's extremely hot. Stay hydrated and avoid too much sun. "

    elif temp_c >= 28:
        advice += "It's warm today. Wear light clothes. "

    elif temp_c >= 18:
        advice += "The weather is pleasant. Great day to go outside! "

    elif temp_c >= 10:
        advice += "It's a little cool. A light jacket is recommended. "

    else:
        advice += "It's cold outside. Wear a warm coat. "

    if rain >= 70:
        advice += "There is a high chance of rain, so take an umbrella."

    elif rain >= 30:   
      advice += "There might be some rain later today."

    else:
        advice += "Rain is unlikely today."

    # -------------------- Display --------------------
    print("\n🌍 WEATHER REPORT")
    print("="*35)
    print("📍 City:", city.title(), ",", country)
    print(f"🌡 Temperature : {temp_c}°C | {temp_f}°F")
    print(f"💧 Humidity    : {humidity}%")
    print(f"💨 Wind Speed  : {wind} km/h")
    print(f"☔ Rain Chance : {rain}%")
    print("\n🤖 AI Advice:")
    print(advice)

    print("\n📅 7-Day Forecast")
    print("-"*35)

    for i in range(7):
        high = daily["temperature_2m_max"][i]
        low = daily["temperature_2m_min"][i]
        rain_p = daily["precipitation_probability_max"][i]

        print(
            f"{daily['time'][i]} | "
            f"High: {high}°C | "
            f"Low: {low}°C | "
            f"Rain: {rain_p}%"
        )

    # -------------------- Map --------------------
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker(
        [lat, lon],
        popup=f"{city.title()}, {country}"
    ).add_to(m)

    display(m)

    # -------------------- Voice Output --------------------
    message = f"""
    The current weather in {city} is as follows.
    Temperature is {temp_c} degrees Celsius,
    or {temp_f} degrees Fahrenheit.
    Humidity is {humidity} percent.
    Wind speed is {wind} kilometers per hour.
    The chance of rain today is {rain} percent.
    {advice}
    """

    speak(message)
     

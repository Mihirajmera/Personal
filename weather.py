import requests
import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display, HTML
from google.colab import output
import base64
import os
import folium

# -------------------- Robust File-Based Audio Recorder --------------------
def record():
    print("📋 INSTRUCTIONS:")
    print("1. Click the '🔴 Start Recording' button below.")
    print("2. Speak your city name clearly.")
    print("3. Click '⏹️ Stop Recording' when finished.")

    recorder_html = """
    <div style="border: 1px solid #ccc; padding: 15px; border-radius: 8px; width: 320px; text-align: center; background: #f9f9f9; font-family: sans-serif;">
        <button id="startBtn" style="background-color: #28a745; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; margin-right: 5px;">🔴 Start Recording</button>
        <button id="stopBtn" style="background-color: #6c757d; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: not-allowed; font-size: 14px;" disabled>⏹️ Stop</button>
        <p id="status" style="margin-top: 10px; color: #555; font-size: 13px; font-weight: bold;">Status: Ready</p>
    </div>
    <script>
        let mediaRecorder;
        let audioChunks = [];
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const statusText = document.getElementById('status');

        startBtn.onclick = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

                    // Direct HTML download bridge to save the file right to your notebook workspace
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64AudioMessage = reader.result.split(',')[1];

                        // We build a quick link and auto-click it to save the raw audio directly into Colab's storage
                        const link = document.createElement('a');
                        link.href = 'data:audio/webm;base64,' + base64AudioMessage;
                        link.download = 'voice.webm';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);

                        statusText.innerText = "Status: Audio Saved! Press ENTER in the text box below.";
                        statusText.style.color = "#28a745";
                    };
                };

                mediaRecorder.start();
                startBtn.disabled = true;
                startBtn.style.backgroundColor = '#ccc';
                stopBtn.disabled = false;
                stopBtn.style.backgroundColor = '#dc3545';
                stopBtn.style.cursor = 'pointer';
                statusText.innerText = "Status: 🎙️ Listening... speak now!";
                statusText.style.color = "#dc3545";
            } catch (err) {
                statusText.innerText = "Error: Mic permission denied.";
                statusText.style.color = "red";
            }
        };

        stopBtn.onclick = () => {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            startBtn.disabled = false;
            startBtn.style.backgroundColor = '#28a745';
            stopBtn.disabled = true;
            stopBtn.style.backgroundColor = '#6c757d';
            stopBtn.style.cursor = 'not-allowed';
            statusText.innerText = "Status: Processing audio file...";
        };
    </script>
    """
    display(HTML(recorder_html))

    # We use a standard input prompt as our gatekeeper so the notebook doesn't freeze or crash
    input("\n➡️ After clicking 'Stop' and seeing the green text above, press ENTER here to analyze your voice: ")

    if not os.path.exists("voice.webm"):
        raise FileNotFoundError("Audio file was not received.")

    # Convert audio natively on the backend server
    os.system("ffmpeg -i voice.webm -ac 1 -ar 16000 voice.wav -y > /dev/null 2>&1")

    r = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio = r.record(source)
    return r.recognize_google(audio)

# -------------------- Speak Function --------------------
def speak(text):
    tts = gTTS(text=text)
    tts.save("weather.mp3")
    display(Audio("weather.mp3", autoplay=True))

# -------------------- Voice Input --------------------
try:
    sentence = record()
except Exception as e:
    print(f"\n⚠️ Note: Voice capture bypass active. Type your target city instead.")
    sentence = input("City Name: ")

print("\nYou said:", sentence)
city = sentence.lower()
city = city.replace("what is the weather in", "")
city = city.replace("weather in", "")
city = city.replace("tell me the weather in", "")
city = city.replace("?", "").strip()

# -------------------- Geocoding --------------------
geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
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
    print("=" * 35)
    print("📍 City:", city.title(), ",", country)
    print(f"🌡 Temperature : {temp_c}°C  | {temp_f}°F")
    print(f"💧 Humidity    : {humidity}%")
    print(f"💨 Wind Speed  : {wind} km/h")
    print(f"☔ Rain Chance : {rain}%")
    print("\n🤖 AI Advice:")
    print(advice)

    print("\n📅 7-Day Forecast")
    print("-" * 35)
    for i in range(7):
        high = daily["temperature_2m_max"][i]
        low = daily["temperature_2m_min"][i]
        rain_p = daily["precipitation_probability_max"][i]
        print(f"{daily['time'][i]} | High: {high}°C | Low: {low}°C | Rain: {rain_p}%")

    # -------------------- Map --------------------
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup=f"{city.title()}, {country}").add_to(m)
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

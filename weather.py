import requests
import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display, HTML
from google.colab import output
import base64
import os
import folium

# -------------------- Foolproof HTML5 Audio Recorder --------------------
def record():
    print("🎤 Click the 'Start Recording' button below, speak your city, then wait 5 seconds...")
    
    # Custom HTML5/JS Audio Capture Widget that forces browser hardware communication
    recorder_html = """
    <div style="border: 1px solid #ccc; padding: 15px; border-radius: 8px; width: 300px; text-align: center; background: #f9f9f9; font-family: sans-serif;">
        <button id="startBtn" style="background-color: #28a745; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 14px;">🔴 Start Recording</button>
        <p id="status" style="margin-top: 10px; color: #555; font-size: 13px;">Ready to record...</p>
    </div>
    <script>
        var startBtn = document.getElementById('startBtn');
        var statusText = document.getElementById('status');
        
        startBtn.onclick = async () => {
            try {
                var stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                var recorder = new MediaRecorder(stream);
                var chunks = [];
                
                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = async () => {
                    var blob = new Blob(chunks, { type: 'audio/webm' });
                    var reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = () => {
                        google.colab.kernel.invokeFunction('notebook.save_audio', [reader.result], {});
                    };
                    statusText.innerText = "Processing audio...";
                };
                
                recorder.start();
                startBtn.disabled = true;
                startBtn.style.backgroundColor = '#dc3545';
                startBtn.innerText = "🎙️ Listening...";
                statusText.innerText = "Recording for 5 seconds...";
                
                setTimeout(() => {
                    recorder.stop();
                    stream.getTracks().forEach(track => track.stop());
                    statusText.innerText = "Done recording! Analyzing text...";
                }, 5000);
            } catch(e) {
                statusText.innerText = "Error: Mic access denied. Check your browser address bar settings.";
            }
        };
    </script>
    """
    
    audio_data = None
    
    def save_audio(base64_string):
        nonlocal audio_data
        audio_data = base64_string
        
    output.register_callback('notebook.save_audio', save_audio)
    display(HTML(recorder_html))
    
    # Wait until the user finishes speaking and the audio string returns
    import time
    while audio_data is None:
        time.sleep(0.5)
        
    # Convert and decode base64 audio
    binary = base64.b64decode(audio_data.split(",")[1])
    with open("voice.webm", "wb") as f:
        f.write(binary)
        
    # Standard fallback audio conversion via ffmpeg directly
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
    print(f"\n⚠️ Quick Note: System couldn't convert voice data cleanly. Parsing typing prompt...")
    sentence = input("Type the city name instead: ")

print("\nYou said:", sentence)
city = sentence.lower()
city = city.replace("what is the weather in", "")
city = city.replace("weather in", "")
city = city.replace("tell me the weather in", "")
city = city.replace("?", "").strip()

# -------------------- Geocoding --------------------
geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?

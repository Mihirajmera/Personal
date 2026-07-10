import torch
import requests
import folium
import random

from transformers import pipeline
from diffusers import AutoPipelineForText2Image
from gtts import gTTS

from IPython.display import Audio, display
from textblob import TextBlob


# ===============================
# LOAD AI MODELS
# ===============================

print("Loading AI models...")

text_ai = pipeline(
    "text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    device_map="auto"
)


print("Loading image AI...")

image_ai = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16
)

if torch.cuda.is_available():
    image_ai.to("cuda")


print("AI Studio Ready 🚀")


# ===============================
# TEXT TO SPEECH
# ===============================

def speak(text):

    print("\n🔊", text)

    audio = gTTS(
        text=text,
        lang="en"
    )

    audio.save("speech.mp3")

    display(
        Audio(
            "speech.mp3",
            autoplay=True
        )
    )


# ===============================
# AI TEXT GENERATOR
# ===============================

def generate(prompt):

    result=text_ai(
        prompt,
        max_new_tokens=200,
        temperature=0.8,
        do_sample=True
    )

    return result[0]["generated_text"]



# ===============================
# JOKE GENERATOR
# ===============================

def joke():

    topic=input(
        "Topic for joke: "
    )

    prompt=f"""
Create a funny joke about {topic}.
Only write the joke.
"""

    answer=generate(prompt)

    print(answer)
    speak(answer)



# ===============================
# STORY GENERATOR
# ===============================

def story():

    topic=input(
        "Story idea: "
    )

    prompt=f"""
Write a creative short story about {topic}.
Include characters, adventure and ending.
"""

    answer=generate(prompt)

    print(answer)
    speak(answer)



# ===============================
# SONG WRITER
# ===============================

def song():

    topic=input(
        "Song topic: "
    )

    prompt=f"""
Write original song lyrics about {topic}.

Include:
Verse 1
Chorus
Verse 2

Only output lyrics.
"""

    answer=generate(prompt)

    print(answer)

    speak(answer)



# ===============================
# IMAGE GENERATOR
# ===============================

def image():

    prompt=input(
        "Describe image: "
    )

    result=image_ai(
        prompt,
        num_inference_steps=2,
        guidance_scale=0
    )

    img=result.images[0]

    display(img)

    img.save(
        "AI_Image.png"
    )


# ===============================
# WEATHER
# ===============================

def weather():

    city=input(
        "City name: "
    )

    geo=requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()


    if "results" not in geo:
        print("City not found")
        return


    place=geo["results"][0]

    lat=place["latitude"]
    lon=place["longitude"]


    data=requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,wind_speed_10m"
        "&daily=precipitation_probability_max"
    ).json()


    temp=data["current"]["temperature_2m"]

    rain=data["daily"]["precipitation_probability_max"][0]

    advice=""

    if temp>30:
        advice="It is hot. Stay hydrated."

    elif temp<10:
        advice="It is cold. Wear a jacket."

    else:
        advice="The weather is pleasant."


    report=f"""
Weather in {city}.

Temperature:
{temp} Celsius.

Rain chance:
{rain} percent.

Advice:
{advice}
"""


    print(report)

    speak(report)


    m=folium.Map(
        [lat,lon],
        zoom_start=10
    )

    folium.Marker(
        [lat,lon],
        popup=city
    ).add_to(m)

    display(m)



# ===============================
# SENTIMENT
# ===============================

def sentiment():

    text=input(
        "Enter sentence: "
    )

    score=TextBlob(text).sentiment.polarity


    if score>0:
        result="Positive 😊"

    elif score<0:
        result="Negative 😔"

    else:
        result="Neutral 😐"


    print(result)
    speak(result)



# ===============================
# MAIN MENU
# ===============================


while True:

    print("""
===============================
🤖 AI FUN STUDIO
===============================

1 😂 Joke Generator

2 📖 Story Generator

3 🎵 Song Writer

4 🎨 Image Generator

5 🌦 Weather Assistant

6 😊 Sentiment Analyzer

7 ❌ Exit

===============================
""")


    choice=input(
        "Choose: "
    )


    if choice=="1":
        joke()

    elif choice=="2":
        story()

    elif choice=="3":
        song()

    elif choice=="4":
        image()

    elif choice=="5":
        weather()

    elif choice=="6":
        sentiment()

    elif choice=="7":
        print("Goodbye 👋")
        break

    else:
        print("Invalid choice")

# ==========================================
# AI Virtual Assistant
# Sentiment + Text Generation + Text Speech
# Google Colab Version
# ==========================================

from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
from IPython.display import Audio, display
import os


# ------------------------------------------
# Load AI Model
# ------------------------------------------

print("Loading AI model... (First time may take 30-60 seconds)")

generation = pipeline(
    "text-generation",
    model="gpt2"
)

print("AI Assistant Ready!\n")


# ------------------------------------------
# Sentiment Analysis
# ------------------------------------------

def sentiment_analysis(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        mood = "😊 Positive"

    elif polarity < -0.2:
        mood = "😔 Negative"

    else:
        mood = "😐 Neutral"

    return mood



# ------------------------------------------
# Text To Speech
# ------------------------------------------

def speak(text):

    tts = gTTS(
        text=text,
        lang="en"
    )

    file = "assistant_voice.mp3"

    tts.save(file)

    display(
        Audio(
            file,
            autoplay=True
        )
    )



# ------------------------------------------
# AI Text Generation
# ------------------------------------------

def generate_text(prompt):

    response = generation(
        prompt,
        max_length=120,
        do_sample=True,
        temperature=0.7,
        num_return_sequences=1
    )

    return response[0]["generated_text"]



# ------------------------------------------
# Main Assistant Loop
# ------------------------------------------

while True:

    print("\n==============================")
    print(" 🤖 AI Virtual Assistant")
    print("==============================")

    print("1. Sentiment Analysis")
    print("2. AI Text Generation")
    print("3. Exit")


    choice = input("\nChoose an option: ")



    # --------------------------------------
    # Sentiment Analysis
    # --------------------------------------

    if choice == "1":

        text = input(
            "\nHow are you feeling today?\n\n> "
        )

        mood = sentiment_analysis(text)

        print(
            "\nDetected Sentiment:",
            mood
        )


        if "Positive" in mood:

            response = (
                "That's wonderful! "
                "Keep maintaining a positive mindset."
            )


        elif "Negative" in mood:

            response = (
                "I'm sorry you are feeling this way. "
                "Remember, difficult times pass."
            )


        else:

            response = (
                "Thank you for sharing your thoughts."
            )


        print(
            "\nAssistant:",
            response
        )

        speak(response)



    # --------------------------------------
    # Text Generation
    # --------------------------------------

    elif choice == "2":

        prompt = input(
            "\nWhat should I write about?\n\n> "
        )


        print(
            "\nGenerating response..."
        )


        result = generate_text(prompt)


        print(
            "\nAI Generated Text:\n"
        )

        print(result)


        speak(result)



    # --------------------------------------
    # Exit
    # --------------------------------------

    elif choice == "3":

        goodbye = (
            "Goodbye! "
            "Have a great day."
        )

        print(goodbye)

        speak(goodbye)

        break



    else:

        print(
            "\nInvalid option. Try again."
        )

from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
from IPython.display import Audio, display

print("Loading AI models... (This may take 30-60 seconds the first time)")
generation = pipeline("text-generation", model="facebook/bart-large-cnn")
print("AI Assistant Ready!\n")


# -----------------------------
# Sentiment Analysis
# -----------------------------
def sentiment_analysis(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        mood = "😊 Positive"
    elif polarity < -0.2:
        mood = "😔 Negative"
    else:
        mood = "😐 Neutral"

    return mood


# -----------------------------
# Text to Speech
# -----------------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("assistant.mp3")
    display(Audio("assistant.mp3", autoplay=True))


# -----------------------------
# Main Assistant
# -----------------------------
while True:

    print("\n==============================")
    print(" AI Virtual Assistant")
    print("==============================")
    print("1. Sentiment Analysis")
    print("2. News/Text generation")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    # -------------------------
    # Sentiment Analysis
    # -------------------------
    if choice == "1":

        text = input("\nHow are you feeling today?\n\n> ")

        mood = sentiment_analysis(text)

        print("\nDetected Sentiment:", mood)

        if "Positive" in mood:
            response = "That's wonderful! Keep smiling."
        elif "Negative" in mood:
            response = "I'm sorry you're feeling that way. Tomorrow is a new day."
        else:
            response = "Thank you for sharing your thoughts."

        print("Assistant:", response)
        speak(response)

    # -------------------------
    # generation
    # -------------------------
    elif choice == "2":

        print("\nPaste a news article or any long paragraph.")
        article = input("\nText:\n")

        print("\nGenerating summary...\n")

        summary = generation(
            article,
            max_length=60,
            min_length=20,
            do_sample=False
        )

        result = summary[0]["summary_text"]

        print("Summary:\n")
        print(result)

        speak("Here is the summary.")
        speak(result)

    # -------------------------
    # Exit
    # -------------------------
    elif choice == "3":

        speak("Goodbye. Have a great day.")
        print("\nGoodbye!")
        break

    else:
        print("\nInvalid choice.")

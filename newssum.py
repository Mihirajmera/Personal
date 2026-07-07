# ==========================================
# 🤖 AI Virtual Assistant 
# ==========================================

from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
from IPython.display import Audio, display


# ------------------------------------------
# Load AI Model
# ------------------------------------------

print("Loading AI model... Please wait.")

generation = pipeline(
    "text-generation",
    model="gpt2"
)

print("✅ AI Assistant Ready!\n")



# ------------------------------------------
# Text To Speech Function
# ------------------------------------------

def speak(text):

    try:

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

    except Exception as e:

        print("TTS Error:", e)



# ------------------------------------------
# Sentiment Analysis
# ------------------------------------------

def sentiment_analysis(text):

    polarity = TextBlob(text).sentiment.polarity


    if polarity > 0.2:

        return (
            "😊 Positive",
            "That's great! Keep spreading positivity."
        )


    elif polarity < -0.2:

        return (
            "😔 Negative",
            "I understand. Stay strong, tomorrow can be better."
        )


    else:

        return (
            "😐 Neutral",
            "Thanks for sharing your thoughts."
        )



# ------------------------------------------
# AI Text Generation
# ------------------------------------------

def generate_text(prompt):

    result = generation(
        prompt,
        max_length=120,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"]



# ------------------------------------------
# AI Story Generator
# ------------------------------------------

def generate_story(topic):

    prompt = f"""

Create an exciting short story for teenagers.

Topic:
{topic}

Include:
- Characters
- Problem
- Adventure
- Ending

"""

    result = generation(
        prompt,
        max_length=250,
        do_sample=True,
        temperature=0.9
    )

    return result[0]["generated_text"]



# ------------------------------------------
# AI Quiz Generator
# ------------------------------------------

def generate_quiz(topic):

    prompt = f"""

Create a fun quiz about:

{topic}

Make:
- 5 multiple choice questions
- Options
- Correct answers

"""

    result = generation(
        prompt,
        max_length=300,
        do_sample=True,
        temperature=0.8
    )

    return result[0]["generated_text"]



# ------------------------------------------
# Main Assistant
# ------------------------------------------

while True:


    print("\n==============================")
    print("🤖 AI Virtual Assistant")
    print("==============================")

    print("1. Sentiment Analysis 😊")
    print("2. AI Text Generation ✍️")
    print("3. Story Generator 📖")
    print("4. Quiz Generator 🧠")
    print("5. Exit 🚪")


    choice = input(
        "\nChoose an option: "
    )



    # -----------------------------
    # Sentiment
    # -----------------------------

    if choice == "1":

        text = input(
            "\nHow are you feeling today?\n> "
        )


        mood, response = sentiment_analysis(text)


        output = (
            f"Your emotion is {mood}. "
            f"{response}"
        )


        print("\nAssistant:")
        print(output)


        speak(output)



    # -----------------------------
    # Text Generation
    # -----------------------------

    elif choice == "2":

        prompt = input(
            "\nWhat should I write about?\n> "
        )


        print(
            "\nGenerating..."
        )


        answer = generate_text(prompt)


        print("\nAI:")
        print(answer)


        speak(answer)



    # -----------------------------
    # Story Generator
    # -----------------------------

    elif choice == "3":

        topic = input(
            "\nGive me a story idea:\n> "
        )


        print(
            "\nCreating story..."
        )


        story = generate_story(topic)


        print("\nStory:")
        print(story)


        speak(story)



    # -----------------------------
    # Quiz Generator
    # -----------------------------

    elif choice == "4":

        topic = input(
            "\nEnter quiz topic:\n> "
        )


        print(
            "\nCreating quiz..."
        )


        quiz = generate_quiz(topic)


        print("\nQuiz:")
        print(quiz)


        speak(quiz)



    # -----------------------------
    # Exit
    # -----------------------------

    elif choice == "5":

        message = (
            "Goodbye! "
            "Thank you for using the AI assistant."
        )

        print(message)

        speak(message)

        break



    else:

        message = (
            "Invalid option. "
            "Please try again."
        )

        print(message)

        speak(message)

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from google.cloud import speech

# Set up the Google Cloud Speech-to-Text client
client = speech.SpeechClient()

def recognize_speech_from_microphone():
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Record the audio from the microphone
    with sr.Microphone() as source:
        st.write("Listening for the word, please speak...")
        audio = recognizer.listen(source)

    try:
        # Use Google Web Speech API to recognize the audio
        recognized_text = recognizer.recognize_google(audio)
        st.write(f"Recognized Speech: {recognized_text}")
        return recognized_text.lower()
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def pronounce_word(word):
    """Function to pronounce a word using gTTS (Google Text-to-Speech)."""
    myobj = gTTS(text=word, lang='en', slow=False)
    filename = f"{word}.mp3"
    myobj.save(filename)
    st.audio(filename, format="audio/mp3")  # Stream the pronunciation audio

def check_spelling(word, user_input):
    """Check if the typed word and spoken word match."""
    if word.lower() == user_input.lower():
        st.write(f"Correct! The word was {word}.")
    else:
        st.write(f"Incorrect. The word was {word}. Please try again.")

# Streamlit UI
st.title("Spelling Bee: Type and Say the Word")

# Option 1: Upload a list of words or input them directly
uploaded_file = st.file_uploader("Upload a file with words", type=["txt"])
if uploaded_file is not None:
    # Read words from uploaded file
    word_list = [line.decode("utf-8").strip() for line in uploaded_file.readlines()]
else:
    # Alternatively, let user input the list
    user_input = st.text_input("Enter a list of words (comma separated):")
    if user_input:
        word_list = [word.strip() for word in user_input.split(',')]
    else:
        word_list = []

# If word list is available, start the spelling bee
if word_list:
    for word in word_list:
        st.write(f"Now spelling the word: {word}")

        # Pronounce the word
        pronounce_word(word)

        # Get the user typed input
        typed_input = st.text_input(f"Please type the word you just heard:")

        # Get the user speech input
        spoken_input = None
        if st.button("Click to Speak the Word"):
            spoken_input = recognize_speech_from_microphone()

        # Once both typed and spoken input are available, check the spelling
        if typed_input and spoken_input:
            check_spelling(word, typed_input)
            check_spelling(word, spoken_input)

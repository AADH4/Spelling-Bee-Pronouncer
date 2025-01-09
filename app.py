import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
import os

# Function to pronounce a list of words
def pronounce_words(word_list, language='en'):
    recognizer = sr.Recognizer()

    for word in word_list:
        # Generate the speech for the word using gTTS
        myobj = gTTS(text=word, lang=language, slow=False)
        audio_file = BytesIO()
        myobj.save(audio_file)
        audio_file.seek(0)

        # Play the audio (synthesized word)
        st.audio(audio_file, format='audio/mp3')

        # Prompt the user to spell the word (type)
        user_input_type = st.text_input(f"Please type the spelling of the word you just heard:")

        # Prompt the user to speak the word into the microphone
        st.write("Now, please say the spelling of the word into your microphone.")
        
        # Record user's speech and recognize it
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)

            try:
                user_input_speech = recognizer.recognize_google(audio)
                st.write(f"You said: {user_input_speech}")
            except sr.UnknownValueError:
                user_input_speech = ""
                st.write("Sorry, I couldn't understand your speech.")
            except sr.RequestError:
                user_input_speech = ""
                st.write("Sorry, there was an issue with the speech recognition service.")

        # Check if both typed and spoken inputs are correct
        if user_input_type.lower() == word.lower() and user_input_speech.lower() == word.lower():
            st.success(f"CORRECT! You spelled '{word}' correctly!")
        else:
            st.error(f"INCORRECT! The correct spelling of the word is: {word}")

# Main program
st.title("Spelling Bee with Speech and Text Input")

# Option to upload a text file with words
uploaded_file = st.file_uploader("Upload a text file with your spelling words", type=["txt"])

# If a file is uploaded, process it
if uploaded_file:
    word_list = [line.strip() for line in uploaded_file.decode('utf-8').splitlines()]
    pronounce_words(word_list)

else:
    # Option 2: Ask the user to type the list of words directly
    user_input = st.text_area("Enter your list of words separated by commas (e.g., apple, banana, cherry):")
    if user_input:
        word_list = [word.strip() for word in user_input.split(',')]
        pronounce_words(word_list)

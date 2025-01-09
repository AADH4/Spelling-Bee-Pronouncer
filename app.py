import streamlit as st
import pyttsx3
import os
import tempfile

def pronounce_and_check_spelling(word_list, language='en'):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    
    # Set the language if needed (default pyttsx3 voices are system dependent)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id)  # Set to the first voice (English)
    
    for word in word_list:
        # Skip empty words
        if not word.strip():
            st.warning("Skipping empty word.")
            continue

        # Generate and save audio using pyttsx3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_filename = temp_audio_file.name
            engine.save_to_file(word, temp_filename)
            engine.runAndWait()

        # Display the audio player for the word
        st.audio(temp_filename, format='audio/mp3')
        
        # Ask the user to type the spelling
        user_input = st.text_input(f"Please spell the word you just heard:", key=word)
        
        # Check if the user input is correct
        if user_input:
            if user_input.lower() == word.lower():
                st.success("Correct!")
            else:
                st.error(f"Incorrect! The correct spelling is: {word}")

        # Remove the temporary audio file
        os.remove(temp_filename)

# Main program
st.title("Spelling Bee Pronunciation App")

user_input = st.text_input("Enter a list of words separated by commas (e.g., apple, banana, cherry):")

if user_input:
    word_list = [word.strip() for word in user_input.split(',')]
    pronounce_and_check_spelling(word_list)

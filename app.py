import streamlit as st
from gtts import gTTS
import os
import time
import hashlib

def pronounce_and_check_spelling(word_list, language='en'):
    for word in word_list:
        # Skip empty words
        if not word.strip():
            st.warning("Skipping empty word.")
            continue

        # Generate a unique short filename
        short_filename = hashlib.md5(word.encode()).hexdigest()[:8] + ".mp3"

        # Generate audio for the word using gTTS
        try:
            tts = gTTS(text=word, lang=language, slow=False)
            tts.save(short_filename)

            # Display the audio player for each word
            st.audio(short_filename, format='audio/mp3')

            # Ensure text input is visible for each word
            user_input = st.text_input(f"Please spell the word you just heard:", key=word, placeholder="Type here")

            # Check if the user input is correct
            if user_input:
                if user_input.lower() == word.lower():
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect! The correct spelling is: {word}")

            os.remove(short_filename)  # Remove the file after playing
            time.sleep(0.7)  # Add a delay to avoid hitting rate limits
        except Exception as e:
            st.error(f"Error processing the word '{word}': {e}")

# Main program
st.title("Spelling Bee Pronunciation App")

# Input words from the user
input_words = st.text_area("Enter a list of words separated by commas:").split(',')
pronounce_and_check_spelling([word.strip() for word in input_words])

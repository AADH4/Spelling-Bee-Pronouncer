import streamlit as st
from gtts import gTTS
import os
def pronounce_and_check_spelling(word_list, language='en'):
    for word in word_list:
        # Generate audio for the word using gTTS
        myobj = gTTS(text=word, lang=language, slow=False)
        filename = f"{word}.mp3"
        myobj.save(filename)
        
        # Display the audio player for each word
        st.audio(filename, format='audio/mp3')
        
        # Ask the user to type the spelling
        user_input = st.text_input(f"Please spell the word you just heard:", key=word)
        
        # Check if the user input is correct
        if user_input:
            if user_input.lower() == word.lower():
                st.success("Correct!")
            else:
                st.error(f"Incorrect! The correct spelling is: {word}")
        
        os.remove(filename)  # Remove the file after playing

# Main program
st.title("Spelling Bee Pronunciation App")
user_input = st.text_input("Enter a list of words separated by commas (e.g., apple, banana, cherry):")
if user_input:
    word_list = [word.strip() for word in user_input.split(',')]
    pronounce_and_check_spelling(word_list)

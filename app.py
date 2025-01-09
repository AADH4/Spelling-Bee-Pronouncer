import streamlit as st
from gtts import gTTS
import os
# Function to pronounce and check spelling
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

# Option 1: Upload a text file with words
uploaded_file = st.file_uploader("Upload your word list (txt file)", type="txt")

if uploaded_file:
    # Read the content of the uploaded file
    word_list = [line.decode("utf-8").strip() for line in uploaded_file.readlines()]
    pronounce_and_check_spelling(word_list)
else:
    # Option 2: Ask the user to type the words directly
    user_input = st.text_input("Enter a list of words separated by commas (e.g., apple, banana, cherry):")
    
    if user_input:
        word_list = [word.strip() for word in user_input.split(',')]
        pronounce_and_check_spelling(word_list)

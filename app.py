import streamlit as st
from gtts import gTTS
from IPython.display import Audio
import os

# Function to pronounce a list of words
def pronounce_words(word_list, language='en'):
    for word in word_list:
        myobj = gTTS(text=word, lang=language, slow=False)
        filename = f"{word}.mp3"
        myobj.save(filename)
        
        # Streamlit Audio player for each word (no word displayed)
        st.audio(filename, format='audio/mp3', use_container_width=True)
        
        os.remove(filename)  # Remove the file after playing

# Main Streamlit app
st.title("Spelling List Pronunciation Program")

# Option 1: Upload a text file with words
uploaded_file = st.file_uploader("Upload a text file with words", type=["txt"])

# If a file is uploaded, process it
if uploaded_file is not None:
    # Read the file content and split it into words
    word_list = [line.decode("utf-8").strip() for line in uploaded_file.readlines()]
    # Pronounce each word in the file
    pronounce_words(word_list)
else:
    # Option 2: Ask the user to type the words directly
    user_input = st.text_input("Type the list of words separated by commas (e.g., apple, banana, cherry):")
    if user_input:
        word_list = [word.strip() for word in user_input.split(',')]
        pronounce_words(word_list)

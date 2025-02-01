import streamlit as st
from gtts import gTTS
import os
import time

def generate_audio_for_words_in_batches(word_list, language='en', batch_size=5, delay=1):
    audio_files = []
    for i in range(0, len(word_list), batch_size):
        batch = word_list[i:i+batch_size]
        
        for word in batch:
            if not word.strip():
                st.warning("Skipping empty word.")
                continue

            try:
                tts = gTTS(text=word, lang=language, slow=False)
                filename = f"{word}.mp3"
                tts.save(filename)
                audio_files.append((word, filename))
            except Exception as e:
                st.error(f"Error processing the word '{word}': {e}")
        
        # Add a delay between batches to avoid rate limiting
        if i + batch_size < len(word_list):
            st.write(f"Generating next batch of words... Please wait.")
            time.sleep(delay)
    
    return audio_files

def display_and_check_spelling(word_list):
    for word, filename in word_list:
        st.audio(filename, format='audio/mp3')
        
        user_input = st.text_input(f"Please spell the word you just heard:", key=word)
        
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
    
    # Generate audio files for all words in batches to avoid rate limits
    audio_files = generate_audio_for_words_in_batches(word_list)
    
    # Display the words and check spelling without delays
    display_and_check_spelling(audio_files)

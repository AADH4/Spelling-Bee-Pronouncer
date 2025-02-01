import streamlit as st
from gtts import gTTS
import os
import time
from concurrent.futures import ThreadPoolExecutor

def generate_audio_for_word(word, language='en'):
    try:
        if not word.strip():
            st.warning("Skipping empty word.")
            return None

        tts = gTTS(text=word, lang=language, slow=False)
        filename = f"{word}.mp3"
        tts.save(filename)
        return (word, filename)
    except Exception as e:
        st.error(f"Error processing the word '{word}': {e}")
        return None

def generate_audio_for_words_in_batches(word_list, language='en', batch_size=5, delay=1):
    audio_files = []
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = [executor.submit(generate_audio_for_word, word, language) for word in word_list]
        for future in futures:
            result = future.result()
            if result:
                audio_files.append(result)
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

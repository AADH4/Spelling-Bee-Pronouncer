from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from google.cloud import speech
import streamlit as st

# Create a custom audio processor
class MyAudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.client = speech.SpeechClient()

    def recv(self, frame):
        # Process the audio frame here (e.g., send to Google Speech-to-Text API)
        audio_data = frame.to_bytes()
        # Use the Google Speech-to-Text API
        # (Ensure the audio data is in the correct format, e.g., WAV, LINEAR16)
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        response = self.client.recognize(config=config, audio=audio)
        
        # Process the response and display transcription
        for result in response.results:
            st.write(f"Recognized text: {result.alternatives[0].transcript}")
        
        return frame  # Return the processed frame

# Streamlit UI
st.title("Spelling Bee with Speech-to-Text")

webrtc_streamer(key="example", audio_processor_factory=MyAudioProcessor)

import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, AudioData
from google.cloud import speech

client = speech.SpeechClient()

# Google Cloud Speech-to-Text function
def transcribe_audio(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    if response.results:
        return response.results[0].alternatives[0].transcript
    return "Sorry, I couldn't understand that."

# WebRTC Audio Processor
class MyAudioProcessor(AudioProcessorBase):
    def recv(self, frame: AudioData) -> AudioData:
        audio_data = frame.to_bytes()
        transcription = transcribe_audio(audio_data)
        st.write(f"Transcription: {transcription}")
        return frame

def main():
    st.title("Spelling Bee App")
    st.write("Please spell the word you just heard:")

    word_to_pronounce = "example"
    st.write(f"Pronouncing the word: {word_to_pronounce}")

    # Start WebRTC stream for recording
    webrtc_streamer(key="example", audio_processor_factory=MyAudioProcessor)

    # Add the spelling check after receiving audio
    if st.button("Check Spelling"):
        user_input = st.text_input("Type the word you just heard:")
        if user_input.lower() == word_to_pronounce.lower():
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct spelling is {word_to_pronounce}")

if __name__ == "__main__":
    main()

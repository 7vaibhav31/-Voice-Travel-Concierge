from gtts import gTTS
import tempfile
import streamlit as st

@st.cache_data(show_spinner=False)
def text_to_speech(text: str):
    tts = gTTS(text=text, lang="en")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

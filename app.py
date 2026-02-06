import streamlit as st
import requests
import re
import os
from speech_to_text import get_text
from text_to_speech import text_to_speech

# ================= LOAD CSS =================
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Travel Concierge",
    page_icon="🎒",
    layout="centered"
)

# ================= CONFIG =================
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MAIN_MODEL = "deepseek/deepseek-chat"
SCALEDOWN_MODEL = "google/gemma-7b-it"

COMMON_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "Travel Concierge"
}

MAX_SPEECH_CHARS = 700

# ================= SESSION STATE =================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "last_plan" not in st.session_state:
    st.session_state.last_plan = ""

if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ================= HEADER =================
col_title, col_clear = st.columns([5, 1])

with col_title:
    st.markdown('<div class="main-title">Travel Concierge</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart trip planning using voice or text</div>', unsafe_allow_html=True)

with col_clear:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []
        st.session_state.last_plan = ""
        st.rerun()

# ================= NLP HELPERS =================
def extract_days(text):
    m = re.search(r"\d+", text)
    return int(m.group()) if m else 3

def extract_source_dest(text):
    m = re.search(r"from\s+(\w+)\s+to\s+(\w+)", text.lower())
    if m:
        return m.group(1).title(), m.group(2).title()
    return "Unknown", "Unknown"

def detect_intent(text):
    text = text.lower()
    if any(k in text for k in ["adventure", "trek", "hiking"]):
        return "Adventure"
    if any(k in text for k in ["luxury", "resort", "premium"]):
        return "Luxury"
    if any(k in text for k in ["budget", "cheap", "low cost"]):
        return "Budget"
    if any(k in text for k in ["relax", "chill", "beach"]):
        return "Relax"
    return "General"

# ================= LLM =================
def call_llm(prompt, model, max_tokens=400):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional travel planner."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    r = requests.post(
        OPENROUTER_BASE_URL,
        headers=COMMON_HEADERS,
        json=payload,
        timeout=30
    )

    return r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else ""

def scale_down(text):
    prompt = f"""
Refine the itinerary:
- Keep day-wise structure
- Keep bullet points
- Add spacing
TEXT:
{text}
"""
    result = call_llm(prompt, SCALEDOWN_MODEL, 300)
    return result if result.strip() else text

def make_speech_friendly(text):
    text = re.sub(r"\*|_|`", "", text)
    text = re.sub(r"\s+", " ", text)
    return text[:MAX_SPEECH_CHARS]

# ================= CHAT HISTORY =================
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= INPUT =================
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask about your trip",
        placeholder="Plan a 3 day trip from Delhi to Goa",
        label_visibility="collapsed"
    )
    send = st.form_submit_button("Send")

# ================= MIC BUTTON =================
if st.button("🎙️ Speak"):
    st.session_state.is_listening = True
    st.rerun()

# ================= MIC LISTENING INDICATOR =================
if st.session_state.is_listening:
    with st.spinner("🎤 Listening..."):
        voice = get_text()

    st.session_state.is_listening = False

    if voice:
        user_input = voice
        send = True

# ================= PROCESS =================
if send and user_input:
    st.session_state.is_processing = True

    st.session_state.chat.append({"role": "user", "content": user_input})

    days = extract_days(user_input)
    source, dest = extract_source_dest(user_input)
    intent = detect_intent(user_input)

    info_block = f"""
**📍 Source:** {source}  
**🏁 Destination:** {dest}  
**🕒 Duration:** {days} days  
**🎯 Intent:** {intent}
"""
    st.session_state.chat.append({"role": "assistant", "content": info_block})

    # 🔄 PROCESSING SPINNER (TEXT + VOICE)
    with st.spinner("🧠 Planning your trip..."):
        raw = call_llm(
            f"""
Create EXACTLY {days} days itinerary.
Use bullet points.
No paragraph text.
""",
            MAIN_MODEL
        )
        final_plan = scale_down(raw)

    st.session_state.last_plan = final_plan
    st.session_state.chat.append({"role": "assistant", "content": final_plan})

    st.session_state.is_processing = False
    st.rerun()

# ================= AUDIO =================
if st.session_state.last_plan:
    st.markdown("---")
    if st.button("🔊 Listen to last plan"):
        with st.spinner("Generating audio..."):
            audio_path = text_to_speech(make_speech_friendly(st.session_state.last_plan))
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path, format="audio/wav")

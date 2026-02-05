import streamlit as st
import requests
import re
from speech_to_text import get_text
from text_to_speech import text_to_speech




# ================= CONFIG =================
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MAIN_MODEL = "deepseek/deepseek-chat"

SCALEDOWN_MODEL = "gpt-4o"   # optional, may fail → safe fallback

COMMON_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "Voice Travel Concierge"
}

MAX_SPEECH_CHARS = 800  # 🔥 major speed-up

# ================= UTILS =================
def extract_days(days_text: str) -> int:
    match = re.search(r"\d+", days_text)
    if match:
        return int(match.group())

    word_map = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    days_text = days_text.lower()
    for word, number in word_map.items():
        if word in days_text:
            return number

    raise ValueError("Days not understood")

def make_speech_friendly(text: str) -> str:
    lines = text.strip().splitlines()
    speech_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.match(r"day\s*\d+", line.lower()):
            num = re.findall(r"\d+", line)[0]
            speech_lines.append(f"Day {num}.")
        elif line.startswith("-"):
            speech_lines.append(line.lstrip("-").strip() + ".")
        else:
            speech_lines.append(line + ".")

    speech = " ".join(speech_lines)
    speech = re.sub(r"\s+", " ", speech)
    speech = re.sub(r"\.\.+", ".", speech)

    return speech.strip()



# ================= LLM CORE =================
def call_llm(prompt: str , model: str, max_tokens: int ) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
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

    if r.status_code != 200:
        st.error(f"LLM error {r.status_code}: {r.text}")
        st.stop()

    return r.json()["choices"][0]["message"]["content"]


def optimize_text(text: str) -> str:
    prompt = f"""
Clean and format the text below.
Do NOT add new information.
Keep meaning same.
Use clean bullet points.

TEXT:
{text}
"""
    try:
        return call_llm(prompt, SCALEDOWN_MODEL, 300)
    except Exception:
        return ""  # fallback handled later


def extract_travel_details(sentence: str) -> str:
    prompt = f"""
Extract travel details.

Sentence: {sentence}

Return ONLY:
Source:
Destination:
Days:
"""
    return call_llm(prompt, MAIN_MODEL, 150)


def generate_itinerary(source: str, destination: str, days: int) -> str:
    prompt = f"""
Create a {days}-day travel itinerary.

From: {source}
Destination: {destination}

Rules:
- Day-wise plan
- 3–4 activities per day
- Short bullet points
- No emojis
- No extra text

Format:

Day 1:
- activity
- activity

Day 2:
- activity
"""
    return call_llm(prompt, MAIN_MODEL, 500)


# ================= UI =================
st.title("🎒 Voice Travel Concierge")

user_input = st.text_input(
    "Type your travel request (or use voice)",
    placeholder="Plan a 3 day trip from Delhi to Paris"
)

if st.button("🎙️ Speak"):
    voice_text = get_text()
    if voice_text:
        user_input = voice_text
        st.success(f"You said: {user_input}")
    else:
        st.warning("Could not understand speech.")

# ================= MAIN FLOW =================
if user_input:
    with st.spinner("Extracting travel details..."):
        output = extract_travel_details(user_input)

    st.subheader("🧾 Extracted Travel Details")
    st.code(output)

    source = destination = days_text = None

    for line in output.splitlines():
        if line.lower().startswith("source"):
            source = line.split(":", 1)[1].strip()
        elif line.lower().startswith("destination"):
            destination = line.split(":", 1)[1].strip()
        elif line.lower().startswith("days"):
            days_text = line.split(":", 1)[1].strip()

    if not (source and destination and days_text):
        st.error("Failed to extract travel details.")
        st.stop()

    try:
        days = extract_days(days_text)
    except ValueError:
        st.error("Could not understand number of days.")
        st.stop()

    with st.spinner("Generating itinerary..."):
        itinerary = generate_itinerary(source, destination, days)

    with st.spinner("Optimizing itinerary..."):
        optimized = optimize_text(itinerary)

    if optimized.strip():
        itinerary = optimized  # safe fallback

    st.subheader("🗺️ Generated Itinerary")
    st.text(itinerary)
    speech = make_speech_friendly(itinerary)

    if st.button("🔊 Listen to itinerary"):
        speech = speech[:MAX_SPEECH_CHARS]  # 🚀 speed-up
        audio_file = text_to_speech(speech)
        st.audio(audio_file, format="audio/mp3")

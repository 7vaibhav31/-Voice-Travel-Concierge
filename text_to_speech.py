import pyttsx3
import os
import time
import uuid

AUDIO_DIR = "audio_outputs"
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text: str) -> str:
    engine = pyttsx3.init()

    # Natural voice tuning
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    filename = f"{uuid.uuid4().hex}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    engine.save_to_file(text, filepath)
    engine.runAndWait()
    engine.stop()

    # ⏳ Wait until file is actually written
    for _ in range(10):
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            break
        time.sleep(0.1)

    return filepath

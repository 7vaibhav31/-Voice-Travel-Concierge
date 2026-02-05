import speech_recognition as sr
import re

def get_text(timeout=5, phrase_time_limit=8):
    """
    Listens from microphone and converts speech to text.
    Returns cleaned, normalized text or None.
    """

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6

    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.4)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        text = recognizer.recognize_google(audio)
        text = text.lower().strip()

        return normalize_speech_text(text)

    except sr.WaitTimeoutError:
        print("⏳ No speech detected.")
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"🌐 Speech API error: {e}")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")

    return None


def normalize_speech_text(text: str) -> str:
    """Fix common speech-to-text issues."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b(\d+)\s*d\b", r"\1 days", text)
    text = re.sub(r"\bday\b", "days", text)
    return text

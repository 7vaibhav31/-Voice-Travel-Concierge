# intents.py
from typing import List

def detect_intents(call_llm, sentence: str) -> List[str]:
    """
    Detect multiple intents from user sentence.
    """
    prompt = f"""
Analyze the user request and identify ALL intents.

Possible intents:
- itinerary
- flights
- hotels
- currency
- translation

Sentence:
{sentence}

Return intents as a comma-separated list.
Example:
itinerary, flights
"""

    output = call_llm(prompt, max_tokens=50)

    intents = [
        intent.strip().lower()
        for intent in output.split(",")
        if intent.strip()
    ]

    return intents

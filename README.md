# Voice-Travel-Concierge



🧳 Travel Concierge

An AI-Powered Voice & Text Travel Planning Assistant



📌 Overview

Travel Concierge is an interactive AI application that helps users plan trips using voice or text input.
The system understands travel requests, extracts key details such as destination and duration, generates a day-wise itinerary, and can also read the plan aloud using text-to-speech.

This project demonstrates the integration of speech recognition, natural language processing, large language models, and text-to-speech in a single Streamlit application.





✨ Features

🎤 Voice Input using microphone

⌨️ Text Input with chatbot-style interaction

🧠 Intent Detection & NLP Processing

Source location

Destination

Trip duration (days)

Travel intent (Adventure, Budget, Luxury, Relax, etc.)

🗺️ Day-wise Travel Itinerary Generation

✂️ Scale-down Processing for clean, readable output

🔊 Text-to-Speech Output (listen to the itinerary)

💬 Chat History Preservation

⏳ Visual indicators for listening and processing

🧹 Clear chat functionality





🏗️ System Architecture
User (Voice / Text)
        ↓
Speech Recognition (optional)
        ↓
NLP Processing (intent & entity extraction)
        ↓
OpenRouter LLM (itinerary generation)
        ↓
Scale-down Model (format & readability)
        ↓
Text-to-Speech (audio output)
        ↓
Streamlit UI (chatbot interface)

🛠️ Technologies Used

Python

Streamlit – Web interface

SpeechRecognition – Speech to text

OpenRouter API – Access to Large Language Models

NLP (Regex + Keyword Matching) – Intent and data extraction

Scale-down LLM – Output refinement

pyttsx3 – Offline text-to-speech

HTML/CSS – UI styling





📂 Project Structure
travel-concierge/
│
├── app.py                 # Main Streamlit application
├── styles.css             # UI styling
├── speech_to_text.py      # Voice input handling
├── text_to_speech.py      # Audio output generation
├── requirements.txt       # Dependencies
└── .streamlit/
    └── secrets.toml       # API keys (not committed)





    

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/travel-concierge.git
cd travel-concierge

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure API Key

Create a file:

.streamlit/secrets.toml


Add:

OPENROUTER_API_KEY = "your_openrouter_api_key"

▶️ Run the Application
streamlit run app.py


🧪 Example Usage

Text Input:

Plan a 3 day adventure trip from Delhi to Goa


Voice Input:

“Plan a four day budget trip from Mumbai to Jaipur”

The system will:

Extract travel details

Detect intent

Generate a structured itinerary

Allow the user to listen to the plan


🎓 Learning Outcomes

This project helped in understanding:

Real-time speech recognition

NLP-based intent extraction

Working with LLM APIs

Managing application state in Streamlit

Improving AI output using secondary processing

Text-to-speech integration

UI/UX feedback for AI applications


🚀 Future Enhancements

PDF export of itinerary

Day-wise audio playback

Multi-language support

Hotel & transport recommendations

Map integration



📜 License

This project is for educational and learning purposes.


👤 Author

Vaibhav Sharma
Computer Science Student


⭐ Acknowledgements

OpenRouter for LLM access

Streamlit for rapid UI development

Open-source Python community

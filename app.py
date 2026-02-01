import streamlit as st
from openai import OpenAI
import tempfile
import os

st.set_page_config(page_title="Anant AI Voice Bot")

st.title("🎙️ Talk to Anant (AI Voice Bot)")
st.write("Click the mic, ask a question, and listen to my response.")

# Load persona
with open("persona.txt", "r") as f:
    PERSONA = f.read()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

audio_input = st.audio_input("Ask me anything")

def speech_to_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return result.text

def get_ai_response(user_text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": PERSONA
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )
    return response.output_text

def text_to_speech(text):
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return audio

if audio_input:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_input.getvalue())
        tmp_path = tmp.name

    user_text = speech_to_text(tmp_path)
    st.markdown(f"**You asked:** {user_text}")

    reply = get_ai_response(user_text)
    st.markdown(f"**Anant:** {reply}")

    st.audio(text_to_speech(reply))

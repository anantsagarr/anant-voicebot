import streamlit as st
from groq import Groq

# ---------- Page setup ----------
st.set_page_config(page_title="Anant AI Voice Bot")
st.title("🎙️ Talk to Anant (AI Agent)")
st.caption("AI agent demo built for interview assessment. Optimized for reliability and zero setup.")
st.write("Ask a question. You can read the answer or listen to it.")

# ---------- Load persona ----------
with open("persona.txt", "r") as f:
    PERSONA = f.read()

# ---------- Groq client ----------
client = Groq()

# ---------- Browser-based Text-to-Speech (FREE) ----------
if st.button("🔊 Speak Answer"):
    st.markdown(
        f"<script>speakText(`{reply}`)</script>",
        unsafe_allow_html=True
    )

# ---------- AI response function ----------
def get_ai_response(user_text):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": user_text}
        ]
    )
    return completion.choices[0].message.content

# ---------- UI ----------
user_text = st.text_input("Ask me anything (example: What is your superpower?)")

if user_text:
    with st.spinner("Thinking..."):
        reply = get_ai_response(user_text)

    st.markdown("### Anant:")
    st.write(reply)

    st.caption("Click the button below to hear the answer.")

    if st.button("🔊 Speak Answer", key="speak_btn"):
        st.markdown(
            f"<script>speakText(`{reply}`)</script>",
            unsafe_allow_html=True
        )

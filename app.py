import os
import streamlit as st
from exa_py import Exa
from dotenv import load_dotenv

# Load environment variables (development only)
load_dotenv()

# Initialize Exa client
EXA_API_KEY = os.getenv("EXA_API_KEY")
if not EXA_API_KEY:
    st.error("EXA_API_KEY not set. Please add it to a .env file.")
    st.stop()

client = Exa(api_key=EXA_API_KEY)

# Page config & custom CSS
st.set_page_config(page_title="Exa.ai ChatBot", page_icon="🤖", layout="centered")
# Load custom CSS for glassmorphism styling
custom_css_path = os.path.join(os.path.dirname(__file__), "static", "custom.css")
if os.path.exists(custom_css_path):
    st.markdown(f"""<style>{open(custom_css_path).read()}</style>""", unsafe_allow_html=True)

st.title("🤖 Exa.ai ChatBot")
st.caption("Powered by Exa.ai, styled with Streamlit & glass‑morphism UI")

# Initialise chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input widget
user_input = st.chat_input("Ask a question…")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking…"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # default model; can be changed later via UI
            messages=st.session_state.history,
            stream=False  # set to True for streaming tokens (requires extra UI work)
        )
    answer = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": answer})

# Render the conversation with premium styling
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"""<div class='chat-container'><b>You:</b> {msg['content']}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='chat-container'><b>Bot:</b> {msg['content']}</div>""", unsafe_allow_html=True)

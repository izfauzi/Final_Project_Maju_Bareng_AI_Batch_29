## Goal Description
Create a responsive, premium‑looking chatbot web app that uses **Exa.ai** as the LLM/backend for generating answers and **Streamlit** for the UI. The app will allow users to type natural‑language queries, send them to Exa.ai, and display the AI‑generated response with smooth animations, dark‑mode styling, and optional source citations.

## User Review Required
> [!IMPORTANT]
> This plan introduces several new dependencies (Streamlit, `exa-py` client, `httpx`). Ensure you are comfortable adding them to your Python environment.
>
> > The app will store the Exa.ai API key in an environment variable (`EXA_API_KEY`). You must provide this key securely; the app will not commit it to source control.

## Open Questions
> [!CAUTION]
> 1. **Exa.ai model selection** – Do you have a preferred model (e.g., `gpt-4o-mini`, `claude-3`, etc.)? If not, we will default to the latest `gpt-4o-mini`.
> 2. **Response streaming** – Should the UI stream tokens as they arrive, or display the full answer at once?
> 3. **Deployment target** – Will you run the app locally, on Streamlit Cloud, or another hosting service?
> 4. **Citation style** – Do you want clickable source links beneath each answer?
> 5. **Rate‑limit handling** – Any specific back‑off strategy you prefer?

## Proposed Changes
---
### Project Scaffold
#### [NEW] exa_chatbot/
```
exa_chatbot/
├─ app.py                 # Streamlit entry point
├─ requirements.txt       # Python dependencies
├─ .streamlit/
│   └─ config.toml        # Theme & UI config (dark mode, custom colors)
├─ static/
│   └─ custom.css         # Additional CSS for glassmorphism effects
└─ .env.example           # Template for environment variables (EXA_API_KEY)
```
---
### requirements.txt
#### [NEW] requirements.txt
```text
streamlit>=1.35
exa-py>=0.2.0
httpx>=0.27
python-dotenv>=1.0
```
---
### Streamlit Configuration
#### [NEW] .streamlit/config.toml
```toml
[theme]
base="dark"
primaryColor="#ff6f61"
backgroundColor="#1e1e2f"
secondaryBackgroundColor="#2e2e3f"
textColor="#fafafa"
font="sans serif"
```
---
### Custom CSS for Premium Look
#### [NEW] static/custom.css
```css
/* Glassmorphism container */
.chat-container {
  backdrop-filter: blur(12px) saturate(180%);
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* Animated typing cursor */
.typing-cursor {
  display: inline-block;
  width: 8px;
  background: #ff6f61;
  animation: blink 1s steps(2, start) infinite;
}
@keyframes blink { to { visibility: hidden; } }
```
---
### Environment Template
#### [NEW] .env.example
```dotenv
# Copy this file to .env and insert your Exa.ai API key
EXA_API_KEY=your_exa_api_key_here
```
---
### Core Application (app.py)
#### [NEW] app.py
```python
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
st.markdown("""<style>""" + open('static/custom.css').read() + """</style>""", unsafe_allow_html=True)

st.title("🤖 Exa.ai ChatBot")
st.caption("Powered by Exa.ai, styled with Streamlit & glass‑morphism UI")

if "history" not not st.session_state:
    st.session_state.history = []

# Input box
user_input = st.chat_input("Ask a question…")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking…"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # <- configurable later
            messages=st.session_state.history,
            stream=False  # change to True for token‑streaming UI (extra work)
        )
    answer = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": answer})

# Render chat history with premium styling
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-container'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><b>Bot:</b> {msg['content']}</div>", unsafe_allow_html=True)
```
---
### Verification Plan
#### Automated Tests
- No unit tests are required for the MVP, but we will run `streamlit run app.py` and perform a smoke test via a headless browser (e.g., Playwright) to verify that the page loads and a sample query returns a response.
#### Manual Verification
1. Install dependencies: `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and insert your Exa.ai API key.
3. Run `streamlit run app.py`.
4. In the browser, type a question (e.g., "What is the tallest mountain?") and verify:
   - The UI uses dark mode with the custom glass‑morphism container.
   - The bot responds within a reasonable time.
   - No API key appears in the UI or source files.
   - Source citations (if returned) are displayed as clickable links.

---
### Future Enhancements (outside current scope)
- Token‑streaming UI with animated typing cursor.
- Chat history persistence (e.g., SQLite).
- Deploy to Streamlit Cloud with secrets management.
- Add a sidebar with model selection, temperature slider, and token limits.

**Please review the above plan and answer the Open Questions.** Once we have confirmation, I will generate the project files and run a quick verification.

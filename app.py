"""
Customer Support Triage Desk
A tiny AI app: paste a customer email, press Run AI, get priority, category and a reply.
Built for the MT1 "Director mindset & vibe coding" session.
"""
import json
import re

import streamlit as st
from groq import Groq

# ---------- 1. Page look ----------
st.set_page_config(page_title="Support Triage Desk", page_icon="📨", layout="centered")
st.title("📨 Customer Support Triage Desk")
st.caption("Paste a customer email. The AI reads it and tells you how urgent it is, what it is about, and how to reply.")

# ---------- 2. The API key (the AI's entry pass) ----------
with st.sidebar:
    st.header("🔑 Setup")
    try:  # a key saved in Streamlit "Secrets" is used if the box is left empty
        saved_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        saved_key = ""
    api_key = st.text_input(
        "Your Groq API key",
        type="password",
        value="",
        placeholder="Paste key here (starts with gsk_)",
        help="Free key from console.groq.com/keys. It stays in your browser session only.",
    ) or saved_key
    model = st.selectbox("AI model", ["openai/gpt-oss-20b", "openai/gpt-oss-120b"],
                         help="20b is faster. 120b is a bit smarter.")
    st.markdown("Get a free key: [console.groq.com/keys](https://console.groq.com/keys)")

# ---------- 3. Sample emails so anyone can try it ----------
SAMPLES = {
    "✍️ Write my own": "",
    "😡 Angry: charged twice": "Hi, I have been charged TWICE for my order #4521 and nobody is answering my calls. "
                              "I need my money back today or I will cancel my account.",
    "📦 Where is my parcel?": "Hello, I ordered a lamp last week and the tracking has not changed for 5 days. "
                             "Can you tell me when it will arrive?",
    "🙂 Small question": "Hi team, just wanted to know if you have a dark mode in the app. Thanks!",
}
choice = st.selectbox("Try a sample email", list(SAMPLES.keys()))
email = st.text_area("Customer email", value=SAMPLES[choice], height=150,
                     placeholder="Paste or type a customer email here...")

# ---------- 4. The instruction we give the AI ----------
INSTRUCTION = """You are a customer support triage assistant.
Read the customer email and answer ONLY with JSON in this exact shape:
{"priority": "High" or "Medium" or "Low",
 "category": "Billing" or "Technical" or "Delivery" or "Account" or "Other",
 "summary": "one short sentence",
 "reply": "a short, polite reply to the customer (2-3 sentences)"}"""


def triage(text: str) -> dict:
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": INSTRUCTION},
                  {"role": "user", "content": text}],
        temperature=0.2,
    )
    raw = resp.choices[0].message.content or ""
    match = re.search(r"\{.*\}", raw, re.S)
    return json.loads(match.group(0) if match else raw)


# ---------- 5. The Run AI button ----------
if st.button("🤖 Run AI", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Please paste your Groq API key in the left panel first. (On phone, tap the > arrow at the top left.)")
    elif not email.strip():
        st.warning("Please type or pick an email first.")
    else:
        with st.spinner("The AI is reading the email..."):
            try:
                result = triage(email)
            except Exception as e:  # keep the message friendly for beginners
                msg = str(e)
                if "401" in msg or "invalid_api_key" in msg.lower():
                    st.error("That API key did not work. Copy it again from console.groq.com/keys.")
                elif "429" in msg:
                    st.error("Too many requests right now. Wait 30 seconds and try again.")
                else:
                    st.error(f"Something went wrong: {msg}")
                st.stop()

        colour = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}.get(result.get("priority"), "⚪")
        c1, c2 = st.columns(2)
        c1.metric("Priority", f"{colour} {result.get('priority', '?')}")
        c2.metric("Category", result.get("category", "?"))
        st.info(f"**Summary:** {result.get('summary', '')}")
        st.subheader("✉️ Suggested reply")
        st.write(result.get("reply", ""))

st.divider()
st.caption("Built by directing AI, not by typing every line. MT1: The Director Mindset & Vibe Coding.")

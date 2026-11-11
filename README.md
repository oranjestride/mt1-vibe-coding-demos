# MT1: The "Director" Mindset & Vibe Coding

Three beginner demos. You describe what you want in plain English, the AI (via Groq) builds it.

| Demo | What you do | Where |
|---|---|---|
| 1. Agentic shift | Connect to AI, build a Hello World page by describing it | `notebooks/Demo1_Hello_World_AI.ipynb` |
| 2. Rapid UI prototyping | Describe a Customer Support Triage Dashboard, AI draws it, then give it a brain | `notebooks/Demo2_Triage_Dashboard_Prototype.ipynb` |
| 3. Notebook to live app | Turn the triage idea into a Streamlit app anyone can open | `notebooks/Demo3_Notebook_to_Live_App.ipynb` + `app.py` |

**You need:** a free Groq API key from https://console.groq.com/keys

**Live app:** https://mt1-triage-desk.streamlit.app

**Run the app on your laptop:**
```
pip install -r requirements.txt
streamlit run app.py
```
No API key is stored in this repository. Each user pastes their own key in the app.

# AI Learning Lab - Starter Kit

A single Streamlit app with three labs powered by **Groq**:
💬 Chatbot · 📄 Document Q&A (RAG) · 🤖 Agent (tool calling)

Read **ROADMAP.md** first - it is your full 26-week plan.

## Folder contents
```
app.py                       # the Streamlit app (all 3 labs)
requirements.txt             # dependencies
ROADMAP.md                   # your step-by-step learning plan
practice/                    # weekly exercises with TODOs
sample_data/sample.txt       # sample doc for the RAG lab
.streamlit/secrets.toml.example
.gitignore
```

## Step 1 - Get a free Groq API key
1. Go to https://console.groq.com and sign up.
2. Open **API Keys** → **Create API Key** → copy it (starts with `gsk_`).

## Step 2 - Run locally
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # Windows: copy ...
# open .streamlit/secrets.toml and paste your key

streamlit run app.py
```
Open http://localhost:8501. (No secrets file? Paste the key in the sidebar instead.)

## Step 3 - Push to GitHub
```bash
git init
git add .
git commit -m "AI Learning Lab"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-learning-lab.git
git push -u origin main
```
`.gitignore` already prevents `secrets.toml` from being uploaded. Double-check on GitHub that it is absent.

## Step 4 - Deploy free on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → pick your repo, branch `main`, main file `app.py`.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. Click **Deploy**. In a few minutes you get a public URL for your resume.

## Troubleshooting
| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the venv and run `pip install -r requirements.txt` |
| 401 / invalid API key | Re-copy the key; no spaces or quotes inside |
| 429 rate limit | Wait a minute or switch to `llama-3.1-8b-instant` |
| Model not found | Models change; see https://console.groq.com/docs/models and edit `MODELS` in `app.py` |
| Agent errors with a model | Use `llama-3.3-70b-versatile` for tool calling |
| Deploy fails | Check `requirements.txt` is at repo root and the main file is `app.py` |

## How to extend it (your homework)
- Phase 3: add chat export, a persona dropdown.
- Phase 4: replace TF-IDF with embeddings (`sentence-transformers` + FAISS).
- Phase 5: add tools (weather API, web search) to `TOOLS` and `TOOL_FUNCS`.

Never share or commit your API key. If it leaks, delete it in the Groq console and create a new one.

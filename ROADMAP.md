# Your AI Learning Roadmap (Beginner → Job-Ready in ~6 Months)

**Assumptions** (change these if they don't match you): complete beginner, ~8-10 hours/week, free resources only,
Groq for LLM API, Streamlit for deployment. If you have less time, double each phase's length.
Free courses and tiers change - check each link's current status before you start.

**How to use this file:** each phase has *Learn → Practice → Build → Checkpoint*.
Do not move on until you pass the checkpoint. Keep a daily log (date, hours, what you learned).

---

## Overview

| Phase | Weeks | Topic | Output |
|---|---|---|---|
| 0 | Week 0 | Setup | Python, VS Code, GitHub, Groq key |
| 1 | 1-4 | Python + data tools | 3 small scripts, 1 data analysis notebook |
| 2 | 5-8 | Machine Learning | Trained, evaluated model on GitHub |
| 3 | 9-12 | LLMs + Generative AI + Prompting | Streamlit chatbot (deployed) |
| 4 | 13-16 | RAG | "Chat with your documents" app (deployed) |
| 5 | 17-20 | Agentic AI | Tool-using agent app (deployed) |
| 6 | 21-26 | Capstone, portfolio, job search | 2 polished projects + resume |

---

## Phase 0 - Setup (Week 0, ~3 hours)

1. Install **Python 3.11+** (python.org) and **VS Code**.
2. Create a free **GitHub** account. Install Git.
3. Create a free **Groq** account at console.groq.com → API Keys → *Create API Key*. Copy it once; store it safely.
4. In a terminal, from this kit's folder:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. Copy `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml` and paste your key.
6. Run `streamlit run app.py`. If the app opens, your setup is done.

**Checkpoint:** the app opens in your browser and the Chatbot lab answers a question.

---

## Phase 1 - Python + Data Tools (Weeks 1-4)

**Goal:** write small programs confidently; read and clean data.

| Week | Learn | Practice |
|---|---|---|
| 1 | Variables, types, conditions, loops, lists, dicts | `practice/week1_python_basics.py` |
| 2 | Functions, files, JSON, error handling, modules, `pip` | Finish all TODOs; build a number-guessing game |
| 3 | NumPy, Pandas (DataFrame, groupby, filter) | `practice/week3_pandas_numpy.py` |
| 4 | Matplotlib, reading CSVs, Git basics (add/commit/push) | Analyse any Kaggle CSV; publish notebook to GitHub |

**Free resources**
- Harvard **CS50P** (Introduction to Programming with Python) - cs50.harvard.edu/python
- **Kaggle Learn**: Python, Pandas, Data Visualization micro-courses - kaggle.com/learn
- freeCodeCamp Python course (YouTube)
- Automate the Boring Stuff with Python (free online book)

**Tools:** VS Code, Jupyter / Google Colab, Git, GitHub.

**Checkpoint (self-test, no googling for 30 min):**
1. Write a function that returns the top 3 most frequent words in a text.
2. Load a CSV, compute average by category, plot a bar chart.
3. Explain list vs dict vs tuple in your own words.

---

## Phase 2 - Machine Learning Fundamentals (Weeks 5-8)

**Goal:** understand the ML workflow: data → split → train → evaluate → improve.

| Week | Learn | Practice |
|---|---|---|
| 5 | What ML is; supervised vs unsupervised; train/test split | `practice/week5_ml_iris.py` |
| 6 | Linear & logistic regression, decision trees, random forest | Predict house prices (Kaggle) |
| 7 | Metrics: accuracy, precision, recall, F1, RMSE; overfitting; cross-validation | Add cross-validation to your model |
| 8 | Feature engineering, pipelines, saving models (`joblib`), intro to neural nets | Kaggle Titanic competition |

**Free resources**
- **Kaggle Learn**: Intro to Machine Learning, Intermediate ML
- **Google Machine Learning Crash Course** (developers.google.com/machine-learning/crash-course)
- **Andrew Ng - Machine Learning Specialization** on Coursera (audit for free)
- **StatQuest** (YouTube) for intuition on every algorithm
- scikit-learn official user guide

**Tools:** scikit-learn, Pandas, Matplotlib, Kaggle notebooks.

**Build - Project 1 (ML):** "Predict-X" - choose a dataset in *your* domain (health, finance, sales, education...).
Clean it, train 3 models, compare metrics, write a README with results and what you'd improve.
Optional: wrap it in a small Streamlit form that predicts from user input.

**Checkpoint:**
- Explain overfitting and two ways to reduce it.
- Why is accuracy misleading on imbalanced data?
- Your Titanic submission scores above the baseline "everyone dies" model.

---

## Phase 3 - LLMs, Generative AI & Prompting (Weeks 9-12)

**Goal:** understand how LLMs work and call them from code.

| Week | Learn | Practice |
|---|---|---|
| 9 | Tokens, context window, temperature, what a transformer does (high level). First Groq API call | `practice/week9_groq_hello.py` |
| 10 | Prompt engineering: system prompts, few-shot, chain-of-thought, JSON output | Do all TODOs in the file; compare temperatures |
| 11 | Chat memory, streaming, error handling and rate limits; open-source vs closed models; hallucinations & safety | Build a CLI chatbot with history |
| 12 | **Streamlit** basics + deploy | Deploy the **Chatbot lab** from `app.py` |

**Free resources**
- **Andrej Karpathy - "Intro to Large Language Models"** and "Let's build GPT" (YouTube)
- **DeepLearning.AI short courses** (ChatGPT Prompt Engineering for Developers, etc.) - deeplearning.ai/short-courses
- **Hugging Face LLM Course** - huggingface.co/learn
- **Groq docs & playground** - console.groq.com/docs
- Streamlit docs & 30 Days of Streamlit

**Groq models (verified in Groq docs, Oct 2026):** `llama-3.3-70b-versatile` (quality), `llama-3.1-8b-instant` (speed),
`openai/gpt-oss-20b`, `openai/gpt-oss-120b`. Groq has rate limits on free usage; if you hit them, wait or switch to the 8B model.

**Build - Project 2:** "AI Tutor Bot" - a Streamlit chatbot with a custom system prompt for *your* domain.
Add: model selector, temperature slider, clear-chat button (all are in `app.py` - extend it).

**Checkpoint:**
- Explain tokens, context window, temperature to a friend.
- Same question, 3 different system prompts → 3 different behaviours, documented.
- Your chatbot is live on a public Streamlit URL.

---

## Phase 4 - RAG: Retrieval-Augmented Generation (Weeks 13-16)

**Goal:** make an LLM answer from *your* documents, with citations.

| Week | Learn | Practice |
|---|---|---|
| 13 | Why RAG; the pipeline: load → chunk → index → retrieve → generate | Read `rag_page()` in `app.py` line by line |
| 14 | Chunking strategies, overlap; keyword search (TF-IDF) vs **embeddings** & vector DBs | Try chunk sizes 300/800/1500; compare answers |
| 15 | Upgrade retrieval to embeddings (`sentence-transformers`) + FAISS/Chroma | Replace TF-IDF in `app.py` with embeddings |
| 16 | Evaluate RAG: question set, groundedness, "I don't know" behaviour | Write 20 test questions + expected answers |

**Free resources**
- DeepLearning.AI: *Building and Evaluating Advanced RAG*, *LangChain: Chat with Your Data*
- LangChain and LlamaIndex official docs/tutorials
- Pinecone Learning Center (free articles on vector search)
- Hugging Face `sentence-transformers` docs

**Tools:** `scikit-learn` TF-IDF (starter) → `sentence-transformers`, `faiss-cpu` or `chromadb`, `pypdf`.
*Note: heavy embedding models make free Streamlit Cloud deploys slower; the starter uses TF-IDF on purpose.*

**Build - Project 3 (flagship):** "Chat with Your Documents" for a real domain (company policies, study notes, legal
FAQ, product manuals). Requirements: multi-file upload, source citations, "I don't know" handling, test set
with measured accuracy in the README.

**Checkpoint:**
- You can explain why retrieval quality limits answer quality.
- Your test set shows ≥ 70% correct, grounded answers (and you know which ones fail and why).
- Deployed and shareable.

---

## Phase 5 - Agentic AI (Weeks 17-20)

**Goal:** LLMs that decide *what to do next* using tools.

| Week | Learn | Practice |
|---|---|---|
| 17 | Tool/function calling; the agent loop (think → act → observe) | Read `agent_page()` in `app.py` |
| 18 | Add your own tools: web search API, weather API, file reader, email draft | Add 2 new tools to `TOOLS` + `TOOL_FUNCS` |
| 19 | Planning, memory, guardrails, max-steps, human approval for risky actions | Add a "confirm before running" step |
| 20 | Frameworks: **LangGraph**, CrewAI; multi-agent basics | Rebuild your agent in LangGraph |

**Free resources**
- **Hugging Face Agents Course** - huggingface.co/learn
- DeepLearning.AI: *AI Agents in LangGraph*, *Functions, Tools and Agents with LangChain*
- Groq docs → Tool Use
- LangGraph docs; Anthropic's "Building effective agents" article

**Build - Project 4 (agent):** "Research/Task Assistant" - e.g. a study-planner agent that searches your documents
(RAG tool), does calculations, checks the date, and produces a weekly plan. Log every tool call visibly.

**Checkpoint:**
- Explain function calling in your own words.
- Your agent handles a 3-step task and stops safely when it fails.
- You can describe 3 ways agents go wrong (loops, wrong tool, hallucinated args) and your mitigation for each.

---

## Phase 6 - Capstone, Portfolio & Job Hunt (Weeks 21-26)

- **Weeks 21-23:** Combine skills into one capstone in your domain (see ideas below). Add auth-less demo, README with
  architecture diagram, screenshots, a 2-minute demo video.
- **Week 24:** Polish GitHub (pinned repos, clean READMEs, `requirements.txt`, no secrets committed). Write 1-2 blog posts
  (dev.to / Medium / LinkedIn) explaining what you built and what failed.
- **Week 25:** Resume + LinkedIn. One page, projects first, each bullet = action + tech + result.
- **Week 26+:** Apply daily (10/week minimum), do mock interviews, contribute to one open-source repo.

### Portfolio projects (aim for 4-5)
1. **Predict-X** - classic ML with honest evaluation (Phase 2)
2. **AI Tutor Bot** - deployed chatbot with custom prompts (Phase 3)
3. **Chat with Your Documents** - RAG with citations + evaluation (Phase 4) ⭐
4. **Task/Research Agent** - tool-using agent with visible traces (Phase 5) ⭐
5. **Domain capstone**, e.g.: customer-support bot over a company FAQ; resume screener (with fairness notes);
   medical-literature explainer; personal finance Q&A over bank statements; SQL-question agent over a database.

**What recruiters look for:** live demo link, clear README, evaluation numbers, handling of failures, clean code.

### Free / low-cost certifications & credentials
Certificates add credibility but projects matter more. Check current prices and free-audit options:
- **Kaggle micro-course certificates** (free)
- **DeepLearning.AI course certificates** (some free, some paid)
- **Hugging Face course completion** (free)
- **Google / Coursera** ML or AI certificates (financial aid or audit available)
- **Microsoft AI-900 (Azure AI Fundamentals)** - low-cost entry cert
- **AWS Certified AI Practitioner** - foundational cloud AI cert
- Later: Azure AI Engineer, AWS ML Specialty, Databricks GenAI

### Career paths
| Role | Focus |
|---|---|
| **GenAI / LLM Application Developer** | RAG, agents, APIs (your main target) |
| **AI Engineer** | Deploying and evaluating AI features in products |
| **Machine Learning Engineer** | Models, pipelines, MLOps |
| **Data Analyst → AI Analyst** | Pandas, SQL, dashboards + LLM automation |
| **AI Automation / Solutions Engineer** | Business workflows with LLMs; good for non-CS backgrounds |
| **Prompt / Conversation Designer** | Prompt design, evaluation, product thinking |

**Domain advantage:** whatever field you come from (finance, healthcare, teaching, marketing, operations),
build projects *in that domain*. "AI + domain knowledge" beats "AI only" for most junior openings.

---

## Weekly Rhythm (≈10 hours)
- 3 × 1.5 h: watch/read lesson
- 3 × 1.5 h: code along + exercises
- 1 × 1 h: review notes, write 5 flashcards
- Weekend: build step of the current project + commit to GitHub

## Progress Tracker (copy into a Google Sheet)
| Week | Topic | Hours | Exercise done? | Checkpoint passed? | Notes |
|---|---|---|---|---|---|

## Common Beginner Mistakes
- Watching videos without coding. Rule: 1 hour watching → 1 hour typing code.
- Committing API keys to GitHub. Always use `secrets.toml` / Streamlit secrets and `.gitignore`.
- Skipping evaluation. "It seems to work" is not a result.
- Jumping to frameworks (LangChain, LangGraph) before understanding the raw API calls.
- Perfectionism: ship ugly, deploy, then improve.

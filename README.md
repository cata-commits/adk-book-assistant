# adk-book-assistant

A book research assistant built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) and Gemini 2.5 Flash. The project evolves across four milestones — from a single agent with mock data to a deployed multi-agent system on Cloud Run.

> Built as a learning project to explore core ADK patterns: tool use, multi-agent orchestration, session state, and cloud deployment.

---

## Architecture

```
              User
               │
         ┌─────▼──────┐
         │ root_agent  │
         └─────┬───────┘
               │
       ┌───────┴────────┐
       │                │
 ┌─────▼──────┐  ┌──────▼──────┐
 │ researcher │  │ recommender │
 └─────┬──────┘  └──────┬──────┘
       │                │
  Open Library     Session state
     API           (saved genres)
```

| Agent         | Responsibility                                            |
| ------------- | --------------------------------------------------------- |
| `root_agent`  | Receives user messages, decides which sub-agent to call   |
| `researcher`  | Looks up factual book data via Open Library API           |
| `recommender` | Gives personalized picks based on saved genre preferences |

---

## Project structure

```
adk-book-assistant/
│
├── agents/
│   ├── __init__.py
│   ├── agent.py                  # root_agent — coordinator
│   ├── researcher/
│   │   ├── __init__.py
│   │   └── agent.py              # researcher_agent
│   └── recommender/
│       ├── __init__.py
│       └── agent.py              # recommender_agent
│
├── tools/
│   ├── __init__.py
│   ├── open_library.py           # search_book, search_author_works
│   └── preferences.py            # get_preferences, set_preferences, remove_preferences
│
├── tests/
│   └── test_open_library.py
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Milestones

| Tag      | What changed                                                                   |
| -------- | ------------------------------------------------------------------------------ |
| `v0.1.0` | Single agent with a mock tool — proves the ADK setup works                     |
| `v1.0.0` | Real Open Library API, tools extracted to their own module, pytest tests added |
| `v2.0.0` | Multi-agent system: researcher + recommender, session state for preferences    |
| `v3.0.0` | Dockerfile, Cloud Run deployment                                               |

---

## Getting started

### Prerequisites

- Python 3.11+
- A [Gemini API key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/adk-book-assistant.git
cd adk-book-assistant

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# open .env and paste your Gemini API key
```

### Run locally

```bash
# Web UI — recommended for exploring the agent
adk web

# Terminal chat
adk run agents

# REST API server
adk api_server --host 0.0.0.0 --port 8080
```

Open `http://localhost:8000` for the web UI. Use the Events panel on the right to see exactly which tools and sub-agents are called for each message.

### Run tests

```bash
pytest tests/ -v
```

---

## How session state works

The recommender agent remembers your genre preferences across turns within a session using ADK's built-in session state — no database needed.

```
"I like sci-fi"           → saves ["sci-fi"]
"also fantasy"            → saves ["sci-fi", "fantasy"]  (merges, no duplicates)
"actually not fantasy"    → saves ["sci-fi"]
"recommend me something"  → reads ["sci-fi"] and suggests accordingly
```

Preferences reset when the session ends. This is intentional for v2 — persistent cross-session storage would require a database and is out of scope for this milestone.

---

## Deployment

This project includes a Dockerfile for Cloud Run deployment.

```bash
# Build the image on Google's servers
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/book-assistant/book-assistant

# Deploy to Cloud Run
gcloud run deploy book-assistant \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/book-assistant/book-assistant \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your_key_here \
  --allow-unauthenticated
```

The API key is never baked into the image — it's injected at deploy time as an environment variable.

### Clean up

```bash
gcloud run services delete book-assistant --region us-central1
```

---

## Tech stack

| Tool                                                             | Purpose                           |
| ---------------------------------------------------------------- | --------------------------------- |
| [Google ADK](https://github.com/google/adk-python)               | Agent framework                   |
| [Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/) | Language model                    |
| [Open Library API](https://openlibrary.org/developers/api)       | Book data — free, no key required |
| [pytest](https://pytest.org)                                     | Unit testing                      |
| [Docker](https://docker.com)                                     | Containerization                  |
| [Cloud Run](https://cloud.google.com/run)                        | Serverless deployment             |

---

## What I learned

- How ADK discovers agents via folder structure and the `root_agent` convention
- Why tool docstrings matter — ADK sends them to the model as the tool description
- How `sub_agents=` works and why agent `description` fields drive routing decisions
- Session state via `ToolContext` for lightweight per-conversation memory
- Why `list[str]` instead of `list` matters when ADK generates Gemini tool schemas
- Containerizing a Python agent with Docker and deploying it to Cloud Run
- Separating concerns: tools in their own module makes them independently testable

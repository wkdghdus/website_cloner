# 🧠 Orchids Challenge – Backend (FastAPI + LangGraph)

This is the backend portion of the Orchids Challenge project, built using **FastAPI** and **LangGraph**, designed for experimentation with agentic workflows and LLM APIs.

---

## 📁 Directory Structure

```
backend/
├── hello.py               # FastAPI server entrypoint
├── pyproject.toml         # (optional) uv config, not required for pip users
├── uv.lock                # lock file for uv users
├── app/
│   ├── __init__.py
│   ├── .env               # environment variables
│   ├── requirements.txt   # Python dependencies (preferred setup method)
│   ├── langgraph.json     # Graph config and entrypoint
│   └── ...                # Agent logic (e.g. agent/graph.py)
```

---

## ⚙️ Setup Instructions

### 🐍 1. Python Version

Ensure Python **3.10+** is installed (recommended 3.11 or later).

### 📦 2. Create Virtual Environment

```bash
cd backend/app
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 📥 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs core dependencies like:

- `fastapi`, `pydantic`, `uvicorn`
- `langchain`, `langgraph`, `langsmith`
- `playwright`, `browserbase`, `bs4` (BeautifulSoup)
- `dotenv` for environment variable loading

> ⚠️ Run `playwright install` after setup if using it for scraping or browser automation.

---
## 🛠 Setup .env File
A .env file is required in backend/app/ to securely store API keys and configuration. Use the provided template below:

```bash
# From the backend/app directory
cp ../../.env.example .env
```

Then fill in your credentials in the new .env file.

---

## 🚀 Run the Server

```bash
cd ..
uvicorn hello:app --reload
```

The API will be live at: [http://localhost:8000](http://localhost:8000)

---

## 🔗 LangGraph Integration

This backend uses `langgraph.json` to specify the agent graph.

### Sample `langgraph.json`:
```json
{
  "dependencies": ["."],
  "graphs": {
    "cloning_agent": "agent/graph.py:graph"
  },
  "env": ".env"
}
```

### To launch the agent (example):
```bash
langgraph run --config app/langgraph.json
```

---

## 🔐 Environment Variables

Create a `.env` file inside `app/`:

```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
LANGCHAIN_API_KEY=your-langchain-key
```

These are accessed via `dotenv` and required by LangChain/LangGraph integrations.

---

## 🧪 API Overview

- `hello.py` defines a basic FastAPI app with CORS enabled for all origins.
- Extend it with custom routes for agent interactions or serve graph outputs.

---

## 🛠 Development Notes

- Keep the `.env` and `langgraph.json` in sync.
- For additional LangGraph graph definitions, edit the `graphs` block in the JSON.
- The backend assumes you're using LangGraph's CLI for interactive testing.

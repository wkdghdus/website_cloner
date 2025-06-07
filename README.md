# 🌸 Orchids Challenge – Fullstack

This project provides a modern fullstack web application template tailored for the Orchids Challenge, with a FastAPI backend and a Next.js + React frontend.

---

## 📦 Project Structure

```
orchids-challenge/
│
├── backend/              # FastAPI backend
│   ├── app/              # Application logic
│   ├── hello.py          # Entrypoint for API with basic setup
│   ├── pyproject.toml    # Backend dependency and project config (uv)
│   └── uv.lock           # uv-managed lockfile
│
├── frontend/             # Next.js frontend
│   ├── package.json      # Frontend dependencies and scripts
│   ├── tsconfig.json     # TypeScript config
│   └── next.config.ts    # Next.js configuration
│
└── README.md             # (You are here)
```

---

## 🛠️ Backend Setup (FastAPI + LangGraph)

### 📚 Requirements
- Python ≥ 3.13
- [`uv`](https://github.com/astral-sh/uv) package manager
- more on `backend/README.md`

### 📦 Install dependencies
```bash
cd backend
uv sync
```

### 🚀 Run the API server
```bash
cd backend/app
python main.py
```

### 🔍 Features
- `hello.py` provides a FastAPI setup with full CORS support.
- `app/requirements.txt` includes advanced AI libraries like:
  - `langchain`, `langgraph`, `langsmith`, `openai`, `anthropic`
  - Browser automation: `playwright`, `browserbase`
  - HTML parsing: `beautifulsoup4`
- `langgraph.json` defines a graph structure:
  - Loads from `agent/graph.py:graph`
  - Uses environment from `.env`

---

## 🎨 Frontend Setup (Next.js + React 19 + TailwindCSS)

### 📚 Requirements
- Node.js ≥ 18
- npm

### 📦 Install dependencies
```bash
cd frontend
npm install
```

### 🚀 Run the development server
```bash
npm run dev
```

### 🧱 Tech Stack
- React 19
- Next.js 15.3.3
- TailwindCSS 4
- TypeScript
- ESLint 9 with Next.js config

---

## 📄 Environment Variables

Backend relies on a `.env` file inside `backend/app/` for LangGraph and API configurations. Make sure to populate it with relevant values for LangGraph and external API services (e.g., OpenAI, Anthropic, etc.).

---

## 🧪 Testing (TBD)

- No test scripts are included yet. You are encouraged to integrate tools like `pytest` for backend or `jest` for frontend.

---

## 🧠 Notes

- The backend is structured to support **agentic graph-based logic** using LangGraph and LangChain.
- The project intentionally allows CORS from all origins for local development; update this before deploying.
- TailwindCSS and TypeScript enhance styling and type safety on the frontend.

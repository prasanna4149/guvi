# Agentic Honey-Pot 🍯


## Overview
Agentic Honey-Pot is a sophisticated counter-scam framework designed to engage scammers with AI-powered personas. By simulating realistic victims (e.g., elderly, confused individuals), the system wastes scammers' time, collects intelligence, and prevents them from targeting real victims.

This repository contains the full stack application:
- **Backend**: FastAPI-powered agent orchestration engine.
- **Frontend**: Modern React interface for monitoring and controlling scams in real-time.

---

## 🏗 Architecture

### Backend (`/scam_honeypot_backend`)
Built with **Python** and **FastAPI**, the backend handles:
- **AI Agent Core**: Manages personas (e.g., "Grandma Edna") and conversation strategies (Stalling, Vulnerable).
- **LLM Integration**: Uses **Groq API** for fast, high-intelligence responses.
- **Scam Detection**: Real-time analysis of scam probability using semantic scoring.
- **API Documentation**: Scalar-powered interactive docs at `/scalar`.

### Frontend (`/scam_honeypot_frontend`)
Built with **React 19** and **Vite**, the frontend features:
- **Live Dashboard**: Watch AI vs. Scammer conversations unfold.
- **Control Panel**: Manually intervene or change agent strategies on the fly.
- **Glassmorphic UI**: A modern, aesthetic interface for security researchers.

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** v18+
- **Python** 3.10+
- **Groq API Key** (Get one at [console.groq.com](https://console.groq.com))

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd scam_honeypot_backend
```

**Installation**
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Mac/Linux)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Configuration**
Create a `.env` file in the `scam_honeypot_backend/` directory:
```env
PROJECT_NAME="Agentic Honey-Pot"
API_KEY="secret-honey-key"
GROQ_API_KEY="your_groq_api_key_here"
SCAM_THRESHOLD=0.7
```

**Run Server**
```bash
python main.py
# Server runs on http://localhost:8000
# Docs available at http://localhost:8000/scalar
```

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd scam_honeypot_frontend
```

**Installation & Run**
```bash
# Install dependencies
npm install

# Start Development Server
npm run dev
```
Access the UI at the URL shown in the terminal (usually `http://localhost:5173`).

---

## 🧩 Features Breakdown

### 🤖 Persona Engine
The system doesn't just "chat"; it embodies a character.
- **Strategies**:
  - `PASSIVE`: Confused, asks simple questions.
  - `VULNERABLE`: "I'm not good with computers..."
  - `ENGAGED`: Feigns interest in sending money.
  - `STALLING`: Delays the conversation purposefully.

### 🛡️ Security & Performance
- **Rate Limiting**: Custom middleware to prevent abuse.
- **API Key Auth**: Secured internal endpoints.
- **FastAPI**: Asynchronous architecture for high concurrency.

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Core** | Python, JavaScript |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | React, Vite, Axios |
| **AI Engine** | Groq (LLM Inference) |
| **Documentation** | Scalar (OpenAPI) |
| **Icons** | Lucide React |

---

## 📝 Usage Guide
1. **Start the Backend**: Ensure the API is running at port 8000.
2. **Start the Frontend**: Open the dashboard in your browser.
3. **Engage**: Start a chat session. The AI will automatically reply based on the active Persona.
4. **Monitor**: Watch the "Scam Score" to see how likely the counter-party is a bad actor.

---

*Project developed for educational and security research purposes.*

## 👥 Contributors
- **Prasanna Patil**
- **Shaunak Chorge**

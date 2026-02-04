# Agentic Honey-Pot Backend

A production-ready, async-first FastAPI backend for detecting scams and extracting intelligence using an autonomous agent.

## Features
- **Scam Detection**: Heuristic and intent analysis to flag scam messages.
- **Autonomous Agent**: Engages scammers with evolving personas (Elderly, Naive Student).
- **Intel Extraction**: automatically extracts UPI IDs, Bank details, Phone numbers, and URLs.
- **Scalar Docs**: Beautiful OpenAPI documentation at `/scalar`.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access Documentation**
   Open [http://localhost:8000/scalar](http://localhost:8000/scalar) to test the API.

## API Usage

**POST** `/api/v1/message`

Headers:
- `X-API-Key`: `secret-honey-key`

Body:
```json
{
  "conversation_id": "conv-12345",
  "message": "Hello sir you have won lottery please send processing fee to upi id scam@bank"
}
```

## Project Structure
- `app/core`: Configuration & Security
- `app/detection`: Scam analysis logic
- `app/agent`: Persona, Strategy, and Generation engine
- `app/extraction`: Intelligence regex & validation
- `app/memory`: State management

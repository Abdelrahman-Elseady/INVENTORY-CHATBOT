Inventory Chatbot API

AI-Powered Inventory & Business Query Service with "Present Query" Output

📌 Overview

Inventory Chatbot is a FastAPI-based backend service that allows users to ask natural language business questions about inventory data.

The system:

- Converts user questions into SQL queries using an LLM (Gemini / OpenAI / etc.)
- Executes raw SQL queries on SQL Server (no ORM)

Returns:

- Natural language answer
- The exact SQL query used ("Present Query")
- Token usage
- Latency
- Provider and model info

This project follows clean architecture principles and uses raw SQL execution for full control.

🏗 Architecture

High-level flow:

```
User
  ↓
FastAPI Endpoint (/api/chat)
  ↓
Chat Service Layer
  ↓
LLM Provider (Gemini / OpenAI)
  ↓
SQL Validator
  ↓
Raw SQL Execution (pyodbc)
  ↓
Formatted Response
```

📂 Project Structure

```
inventory-chatbot/
├── .env
├── requirements.txt
├── README.md
├── list_models.py
└── app/
    ├── main.py
    ├── api/
    │   └── chat.py
    ├── core/
    │   └── config.py
    ├── db/
    │   ├── connection.py
    │   ├── executer.py
    │   └── validator.py
    ├── llm/
    │   ├── prompt_builder.py
    │   └── provider.py
    ├── models/
    │   └── Req_Res_schemas.py
    └── services/
        └── chat_service.py
```

⚙️ Features

- REST API using FastAPI
- LLM-based SQL generation
- Raw SQL execution (no ORM)
- SQL safety validation (SELECT-only enforcement)
- Dynamic answer formatting
- Token usage tracking
- Latency measurement
- Provider switching via environment variables

🔧 Technologies Used

- Python 3.10+
- FastAPI
- Uvicorn
- pyodbc (Raw SQL execution)
- Google Gemini / OpenAI API
- SQL Server
- python-dotenv

🚀 Setup Instructions

1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd inventory-chatbot
```

2️⃣ Create Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

4️⃣ Configure Environment Variables

Create a `.env` file in project root with the following example:

```
# LLM Config
PROVIDER=gemini
MODEL_NAME=gemini-2.5-flash
MODEL_API_KEY=your_api_key_here

# Database Config
DB_SERVER=localhost
DB_DATABASE=InventoryDB
DB_DRIVER=ODBC Driver 17 for SQL Server

# If using SQL Authentication:
# DB_USERNAME=sa
# DB_PASSWORD=your_password
```

_If using Windows Authentication, the system uses `Trusted_Connection=yes` and no username/password is required._

5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:
http://127.0.0.1:8000/docs

📡 API Endpoint

**POST** `/api/chat`

Request Body:

```json
{
  "session_id": "123",
  "user_message": "How many customers do we have?",
  "conversation_history": {}
}
```

Response Example:

```json
{
  "natural_language_answer": "We have a total of 25 customers in the system.",
  "sql_query": "SELECT COUNT(CustomerId) FROM Customers;",
  "token_usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  },
  "latency_ms": 1128,
  "provider": "gemini",
  "model": "gemini-2.5-flash",
  "status": "ok"
}
```

🔒 Security Measures

- SQL queries must start with `SELECT`
- Blocking dangerous keywords: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`
- LLM output validation before execution
- Raw SQL execution isolated in database layer

🧠 Design Decisions

- No ORM used — full control over raw SQL
- Provider-agnostic LLM layer
- Clean separation of concerns:
  - API layer
  - Service layer
  - LLM layer
  - Database layer
- Production-style modular structure

📊 Future Improvements

- Add caching (Redis)
- Add authentication / role-based access
- Add Docker support
- Add query logging table
- Add conversation memory
- Add streaming responses

🎯 Project Purpose

This project demonstrates:

- Backend engineering skills
- Clean architecture design
- LLM integration in real systems
- Secure SQL execution
- AI-powered business intelligence

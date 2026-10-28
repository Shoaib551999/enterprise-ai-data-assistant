# Enterprise AI Data Assistant

### An AI-powered business analytics assistant built with FastAPI, PostgreSQL, Ollama, Qwen2.5, and Streamlit.

## Overview

Business teams often rely on data engineers and analysts to answer relatively straightforward questions about revenue, customers, and product performance. Even when the information is available in a database, retrieving it usually requires writing SQL queries or navigating reporting tools.

I built the Enterprise AI Data Assistant to explore a more accessible way of working with business data.

The application allows users to ask questions in everyday language and receive answers based on actual records stored in PostgreSQL. Instead of requiring users to understand database schemas or write SQL, the system uses a locally hosted language model to interpret their questions and retrieve the appropriate business metrics.

The project brings together backend development, database engineering, large language models, API integration, and interactive data visualization.

## The Problem

Consider an e-commerce business where a manager wants to know:

- Which products generate the highest revenue?
- How much revenue has the business generated?
- Who are our highest-spending customers?
- How many orders have been placed?

These questions are simple from a business perspective, but answering them typically requires someone to query the underlying database.

The goal of this project was to build a practical assistant that makes common business analytics accessible through natural-language questions while maintaining control over database access.

## Solution

The Enterprise AI Data Assistant provides a web-based interface where users can submit business questions.

The application uses Qwen2.5, running locally through Ollama, to identify the user's analytical intent.

That intent is mapped to a predefined SQL query, which is executed against PostgreSQL using a restricted read-only database account.

The results are returned through a FastAPI backend and displayed in Streamlit as tables, charts, and business metrics.

This design allows the application to benefit from natural-language understanding without giving the language model unrestricted control over SQL execution.

## System Architecture

```text
                  Business User
                        |
                        v
               Streamlit Dashboard
                        |
                        v
                  FastAPI Backend
                        |
                        v
               AI Question Processor
                        |
                        v
                Ollama + Qwen2.5
                        |
                        v
              Business Intent Detection
                        |
                        v
                Approved SQL Queries
                        |
                        v
                PostgreSQL Database
                 (Read-Only Access)
                        |
                        v
                Business Analytics
                        |
                        v
             Tables, Charts, and KPIs
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API development |
| PostgreSQL | Relational database and business data |
| SQLAlchemy | Database connectivity and query execution |
| Psycopg | PostgreSQL database driver |
| Ollama | Local LLM runtime |
| Qwen2.5 3B | Natural-language intent classification |
| Streamlit | Interactive web dashboard |
| Pandas | Data processing and visualization preparation |
| Pytest | Automated testing |
| HTTPX | API testing support |

## Key Features

### 1. Natural-Language Business Analytics

Users can ask business questions without writing SQL.

For example:

**User question:**

> Which five products generate the most revenue?

The application interprets the question and identifies the appropriate business intent.

It then executes the corresponding approved SQL query and returns the results.

The current implementation supports four business intents:

- Total revenue
- Total orders
- Top products by revenue
- Top customers by spending

This is an intentionally constrained implementation rather than an unrestricted text-to-SQL system.

### 2. Local LLM Integration

The application uses Qwen2.5 3B through Ollama.

Running the model locally allows the project to demonstrate LLM integration without relying on a paid external inference API.

The model is responsible for understanding the user's question and classifying it into a supported business intent.

It does not directly execute SQL statements.

### 3. PostgreSQL Business Database

The application uses a relational database containing three connected tables:

**Customers**

Stores customer information, including customer names, email addresses, cities, and signup dates.

**Products**

Stores product details, including categories, prices, and inventory quantities.

**Orders**

Stores sales transactions, including customer references, product references, quantities, transaction prices, order status, and order dates.

The database contains simulated e-commerce data used to demonstrate business analytics.

The initial dataset includes:

- 10 customers
- 10 products
- 500 generated sales transactions

The application calculates revenue using completed transactions.

### 4. Read-Only Database Access

One of the key design decisions was separating AI database access from the main application connection.

A dedicated PostgreSQL role, `ai_reader`, was created with restricted permissions.

The AI query engine uses this account to retrieve business data.

The implementation also uses predefined SQL statements rather than executing arbitrary SQL generated by the model.

Additional controls include a database statement timeout and read-only transactions.

These measures provide a foundation for safer database access, although a production deployment would require further security hardening.

### 5. FastAPI Backend

FastAPI provides the interface between the frontend, AI components, and database.

The application exposes endpoints for:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Application information |
| `/health` | GET | Service health check |
| `/analytics/revenue` | GET | Completed-order revenue analytics |
| `/ask` | POST | Predefined business question processing |
| `/ai/ask` | POST | LLM-powered business intent classification and analytics |

FastAPI also provides interactive API documentation through Swagger UI.

### 6. Interactive Streamlit Dashboard

The Streamlit frontend provides a simple interface for business users.

The dashboard includes:

**Executive KPI Cards**

Displays key business metrics, including total revenue, completed orders, and customer count.

**AI Question Interface**

Allows users to submit natural-language business questions.

**Business Analytics Tables**

Displays the results retrieved from PostgreSQL.

**Revenue Visualization**

Provides a bar chart comparing the highest-revenue products.

The frontend communicates with the FastAPI backend to process AI questions.

### 7. Automated Testing

Automated tests were added using Pytest.

The current test suite covers:

- API home endpoint
- API health endpoint
- Revenue analytics endpoint
- Top-products question handling
- Total-revenue question handling
- Unsupported-question handling

The AI assistant tests use mocking to validate application behavior without requiring live LLM inference.

The revenue endpoint test currently requires a running PostgreSQL database populated with the expected schema.

**Current result: Six tests passed across the API and AI test suites.**

## Project Structure

```text
enterprise-ai-data-assistant/
│
├── main.py                 # FastAPI application
├── app.py                  # Streamlit dashboard
├── database.py             # Main database connection
├── ai_database.py          # Restricted AI database connection
├── query_engine.py         # Approved business SQL queries
├── ai_assistant.py         # LLM intent classification
├── llm_engine.py           # Ollama integration
│
├── tests/
│   ├── test_api.py
│   └── test_ai_assistant.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Running the Project Locally

### Prerequisites

Install:

- Python
- PostgreSQL
- Ollama

Download the required language model:

```bash
ollama pull qwen2.5:3b
```

### 1. Clone the Repository

```bash
git clone <repository-url>
cd enterprise-ai-data-assistant
```

Replace `<repository-url>` with the GitHub repository URL after publication.

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Configure the PostgreSQL host, port, database name, and database credentials.

The database must contain the `customers`, `products`, and `orders` tables.

A separate database user with read-only permissions is required for the AI query engine.

**Note:** Database schema creation and sample-data generation are currently manual setup steps. They are not yet automated through migration or seed scripts.

### 5. Start the Backend

```powershell
python -m uvicorn main:app --reload
```

The API will be available at:

`http://localhost:8000/docs`

### 6. Start the Streamlit Dashboard

Open another terminal:

```powershell
python -m streamlit run app.py
```

Open the dashboard at:

`http://localhost:8501`

### 7. Run Tests

```powershell
python -m pytest tests/ -v -p no:cacheprovider
```

The API integration tests require access to the configured PostgreSQL database.

## Example Workflow

A user enters:

> Which five products generate the most revenue?

The system processes the request through the following stages:

**Step 1 — Question Submission**

The Streamlit dashboard sends the question to the FastAPI backend.

**Step 2 — LLM Processing**

Qwen2.5 interprets the question and classifies it as `top products`.

**Step 3 — Query Selection**

The query engine selects the predefined SQL query for product revenue analysis.

**Step 4 — Database Execution**

The application executes the query through the restricted PostgreSQL connection.

**Step 5 — Result Presentation**

The results are returned to Streamlit and displayed as a table and revenue chart.

## Engineering Decisions

Several design decisions shaped this project.

**Using a local language model**

I wanted to explore an AI architecture that could be developed and demonstrated without recurring inference API costs.

**Separating AI access from database administration**

The AI component uses a dedicated read-only database account to reduce the risk associated with database access.

**Using intent classification instead of unrestricted SQL generation**

Rather than allowing the model to produce arbitrary executable queries, I chose to map recognized intents to approved SQL statements.

This limits flexibility but provides more predictable query behavior.

**Separating the backend from the frontend**

FastAPI handles business logic and API requests, while Streamlit handles user interaction and visualization.

This separation makes it easier to test and extend individual components.

## Current Limitations

This project is a functional portfolio MVP, not a production-ready enterprise platform.

The current version has several limitations:

- Supports four predefined business intents.
- Does not yet support unrestricted natural-language-to-SQL generation.
- Uses simulated business data.
- Requires manual database initialization.
- Does not yet include user authentication or authorization.
- Does not currently implement document-based retrieval-augmented generation (RAG).
- Has not been evaluated against a comprehensive LLM accuracy benchmark.
- Requires additional deployment, monitoring, and security work for production use.

These limitations are useful starting points for future improvements.

## Future Enhancements

Potential improvements include:

- Retrieval-augmented generation for internal business documents.
- Additional analytical intents and query templates.
- Date-range and category-based filtering.
- Conversation history and contextual follow-up questions.
- Role-based access control.
- Automated database migrations and sample-data seeding.
- Docker-based deployment.
- Expanded automated tests and CI/CD.
- LLM evaluation and monitoring.

## What I Learned

Building this project helped me understand how different parts of an AI application work together.

The most important learning was that connecting an LLM to a database involves more than generating SQL.

It requires decisions about database permissions, query execution, application boundaries, response handling, and user experience.

I also gained practical experience integrating a locally hosted language model with Python, building REST APIs using FastAPI, designing relational database queries, and presenting analytical results through Streamlit.

The project reinforced the value of keeping AI interpretation separate from database execution.

## Final Thoughts

The Enterprise AI Data Assistant demonstrates how language models can make structured business data easier to access.

Although the current implementation focuses on a small set of predefined analytical questions, it provides a working foundation for more advanced enterprise AI systems.

My focus was on building an end-to-end application where the AI component, backend services, database, and frontend work together to solve a practical business problem.

The result is a functional AI-powered analytics assistant that can be extended with more sophisticated retrieval, reasoning, and data-access capabilities.

---

**Project Type:** AI Engineering | Data Engineering | Backend Development

**Technologies:** Python, FastAPI, PostgreSQL, SQLAlchemy, Ollama, Qwen2.5, Streamlit, Pytest

**Status:** Functional MVP — Local Development
from ai_assistant import ask_ai_assistant
from pydantic import BaseModel
from query_engine import ask_business_question
from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI(
    title="Enterprise AI Data Assistant",
    description="AI-powered assistant for enterprise business data",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Enterprise AI Data Assistant",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-ai-data-assistant"
    }


@app.get("/analytics/revenue")
def get_total_revenue():
    query = text("""
        SELECT
            COUNT(*) AS completed_orders,
            COALESCE(SUM(total_amount), 0) AS total_revenue
        FROM orders
        WHERE order_status = 'Completed'
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().one()

    return {
        "completed_orders": result["completed_orders"],
        "total_revenue": float(result["total_revenue"])
    }
class QuestionRequest(BaseModel):
    question: str

@app.post("/ai/ask")
def ask_ai_question(request: QuestionRequest):
    response = ask_ai_assistant(request.question)
    return response

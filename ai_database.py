import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

AI_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("AI_DB_USER"),
    password=os.getenv("AI_DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5433")),
    database=os.getenv("DB_NAME"),
)

ai_engine = create_engine(
    AI_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"options": "-c statement_timeout=5000"}
)


def test_ai_connection():
    with ai_engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        )
        return result.scalar_one()


if __name__ == "__main__":
    count = test_ai_connection()
    print("AI read-only database connected successfully!")
    print(f"Total orders accessible: {count}")
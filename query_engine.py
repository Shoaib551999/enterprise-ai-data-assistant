from sqlalchemy import text
from ai_database import ai_engine


BUSINESS_QUERIES = {
    "total revenue": """
        SELECT COALESCE(SUM(total_amount), 0) AS total_revenue
        FROM orders
        WHERE order_status = 'Completed'
    """,

    "total orders": """
        SELECT COUNT(*) AS total_orders
        FROM orders
    """,

    "top products": """
        SELECT
            p.product_name,
            SUM(o.quantity) AS units_sold,
            SUM(o.total_amount) AS revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Completed'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 5
    """,

    "top customers": """
        SELECT
            c.customer_name,
            SUM(o.total_amount) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_status = 'Completed'
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC
        LIMIT 5
    """
}


def ask_business_question(question):
    question = question.lower().strip()

    selected_query = None

    for keyword, sql in BUSINESS_QUERIES.items():
        if keyword in question:
            selected_query = sql
            break

    if selected_query is None:
        return {
            "question": question,
            "answer": "I don't understand this question yet.",
            "supported_questions": list(BUSINESS_QUERIES.keys())
        }

    with ai_engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )

            result = connection.execute(
                text(selected_query)
            )

            rows = [dict(row) for row in result.mappings().all()]

    # Convert PostgreSQL Decimal values into JSON-friendly numbers
    from decimal import Decimal

    for row in rows:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)

    return {
        "question": question,
        "data": rows
    }


if __name__ == "__main__":
    question = "What are my top products?"
    response = ask_business_question(question)
    print(response)
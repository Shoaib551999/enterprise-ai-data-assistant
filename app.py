import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ai/ask"

from sqlalchemy import text
from ai_database import ai_engine


def get_dashboard_metrics():
    query = text("""
        SELECT
            (SELECT COALESCE(SUM(total_amount), 0)
             FROM orders
             WHERE order_status = 'Completed') AS total_revenue,

            (SELECT COUNT(*)
             FROM orders
             WHERE order_status = 'Completed') AS completed_orders,

            (SELECT COUNT(*)
             FROM customers) AS total_customers
    """)

    with ai_engine.connect() as connection:
        return dict(connection.execute(query).mappings().one())

st.set_page_config(
    page_title="Enterprise AI Data Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise AI Data Assistant")

st.subheader("📊 Executive Business Overview")

metrics = get_dashboard_metrics()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"${metrics['total_revenue']:,.2f}"
    )

with col2:
    st.metric(
        "📦 Completed Orders",
        f"{metrics['completed_orders']:,}"
    )

with col3:
    st.metric(
        "👥 Total Customers",
        f"{metrics['total_customers']:,}"
    )

st.divider()

st.caption(
    "Ask business questions using AI-powered analytics"
)

st.markdown("""
### Example Questions
- Which five products generate the most revenue?
- What is our total revenue?
- How many orders do we have?
- Who are our top customers?
""")

question = st.text_input(
    "Ask your business question:",
    placeholder="Example: Which products generate the most revenue?"
)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("AI is analyzing your question..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                if "detected_intent" in result:
                    st.success("Analysis completed!")

                    st.write(
                        "**Detected Intent:**",
                        result["detected_intent"]
                    )

                    st.subheader("Business Analytics Results")

                    data = result.get("result", [])

                    if data:
                        st.dataframe(data,width="stretch")

                        if result["detected_intent"] == "top products":
                            st.subheader("📊 Top Products by Revenue")

                            import pandas as pd

                            df = pd.DataFrame(data)

                            st.bar_chart(
                                df.set_index("product_name")["revenue"]
                            )
                    else:
                        st.info("No matching records found.")
                else:
                    st.warning(
                        result.get(
                            "answer",
                            "This question is not supported yet."
                        )
                    )

            except requests.exceptions.RequestException as error:
                st.error(f"Unable to connect to the AI API: {error}")
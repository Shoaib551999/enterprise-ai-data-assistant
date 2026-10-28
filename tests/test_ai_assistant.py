from unittest.mock import patch

from ai_assistant import ask_ai_assistant


def test_top_products_question():
    mock_data = [
        {
            "product_name": "Laptop Pro 15",
            "units_sold": 126,
            "revenue": 163798.74
        }
    ]

    with patch(
        "ai_assistant.classify_question",
        return_value="top products"
    ), patch(
        "ai_assistant.ask_business_question",
        return_value={"data": mock_data}
    ):
        result = ask_ai_assistant(
            "Which products generate the most revenue?"
        )

    assert result["detected_intent"] == "top products"
    assert result["result"] == mock_data


def test_total_revenue_question():
    with patch(
        "ai_assistant.classify_question",
        return_value="total revenue"
    ), patch(
        "ai_assistant.ask_business_question",
        return_value={"data": [{"total_revenue": 250000.00}]}
    ):
        result = ask_ai_assistant(
            "How much revenue did we generate?"
        )

    assert result["detected_intent"] == "total revenue"
    assert result["result"][0]["total_revenue"] == 250000.00


def test_unsupported_question():
    with patch(
        "ai_assistant.classify_question",
        return_value="unsupported"
    ):
        result = ask_ai_assistant(
            "What will the stock market do tomorrow?"
        )

    assert result["answer"] == "This question is not supported yet."
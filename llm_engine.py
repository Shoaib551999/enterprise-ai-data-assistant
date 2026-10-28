from ollama import Client

client = Client(host="http://127.0.0.1:11434")

MODEL_NAME = "qwen2.5:3b"


def ask_llm(question):
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise data analytics assistant. "
                    "Help users understand SQL, databases, and business analytics. "
                    "Give clear, concise answers. "
                    "Do not invent business metrics or claim to have queried "
                    "a database unless actual results are provided."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        options={"temperature": 0}
    )

    return response.message.content


if __name__ == "__main__":
    question = "Explain the difference between revenue and profit."
    answer = ask_llm(question)

    print("\nQuestion:", question)
    print("\nAI Answer:", answer)
import os
from typing import List
from openai import OpenAI

# Ensure your Featherless API key is available
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
if not FEATHERLESS_API_KEY:
    raise ValueError("Missing FEATHERLESS_API_KEY environment variable.")

# Initialize the client for Featherless AI
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=FEATHERLESS_API_KEY,
)

# Choose the model
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"  # You can change this if needed


def build_prompt(question: str, context_chunks: List[str]) -> str:
    """Combine context and question into a structured prompt."""
    context_text = "\n\n---\n\n".join(context_chunks)
    system_text = (
        "You are a helpful assistant. "
        "Use ONLY the provided context to answer the user's question. "
        "If the answer is not in the context, say you don't know."
    )
    user_text = f"Context:\n{context_text}\n\nQuestion: {question}\n\nAnswer concisely and cite context if used."
    return f"{system_text}\n\n{user_text}"


def generate_answer(question: str, context_chunks: List[str]) -> str:
    """Query Featherless AI through OpenAI-compatible SDK."""
    prompt = build_prompt(question, context_chunks)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.0,
    )

    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    context = [
        "Python is a programming language that lets you work quickly and integrate systems more effectively.",
        "Transformers library by Hugging Face provides tools for using pretrained models."
    ]
    question = "What is Python?"
    answer = generate_answer(question, context)
    print("Answer:", answer)

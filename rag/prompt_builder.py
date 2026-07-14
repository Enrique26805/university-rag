def build_prompt(context, question):

    prompt = f"""
You are an AI/ML teaching assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, respond with:
"I don't know based on the provided documents."

Explain concepts clearly and concisely.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt
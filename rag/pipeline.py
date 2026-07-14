from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from llm.generator import generate_answer


def ask(question):

    retrieved_chunks = retrieve_context(question)

    context = ""

    sources = []

    for chunk in retrieved_chunks:

        context += chunk.payload["text"]
        context += "\n\n"

        source = chunk.payload["source"]

        if source not in sources:
            sources.append(source)

    prompt = build_prompt(context, question)

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": sources
    }
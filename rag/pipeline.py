from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from llm.generator import generate_answer


def ask(question):

    # Retrieve the most relevant chunks from Qdrant
    retrieved_chunks = retrieve_context(question)

    context = ""
    sources = []

    # Build a well-structured context for the LLM
    for i, chunk in enumerate(retrieved_chunks, start=1):

        source = chunk.payload["source"]

        context += f"Document {i}\n"
        context += f"Source: {source}\n\n"
        context += chunk.payload["text"]
        context += "\n\n"
        context += "-" * 50
        context += "\n\n"

        # Store unique source names
        if source not in sources:
            sources.append(source)

    # Build the prompt
    prompt = build_prompt(context, question)

    # Generate answer using Ollama
    answer = generate_answer(prompt)

    # Return both the answer and the document sources
    return {
        "answer": answer,
        "sources": sources
    }
from rag.prompt_builder import build_prompt

context = """
Self-attention allows every token in a sequence to attend to every other token.
"""

question = "What is self-attention?"

prompt = build_prompt(context, question)

print(prompt)
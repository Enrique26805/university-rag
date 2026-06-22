from embeddings.embedder import embed_text
from sklearn.metrics.pairwise import cosine_similarity

query = "What problem does ResNet solve?"

chunk = """
Deep neural networks are more difficult to train.
We present a residual learning framework to ease
the training of substantially deeper networks.
"""
unrelated = """
RNNs process sequential data and maintain hidden states.
LSTMs solve the vanishing gradient problem in sequence models.
"""

query_embedding = embed_text(query)
chunk_embedding = embed_text(chunk)
unrelated_embedding = embed_text(unrelated)
similarity = cosine_similarity(
    [query_embedding],
    [chunk_embedding]
)

print(similarity)

similarity = cosine_similarity(
    [query_embedding],
    [unrelated_embedding]
)
print(similarity)
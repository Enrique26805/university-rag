from qdrant_client.models import VectorParams, Distance

from vector_store.qdrant_store import (
    client,
    COLLECTION_NAME
)

if not client.collection_exists(COLLECTION_NAME):

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Collection created")

else:
    print("Collection already exists")
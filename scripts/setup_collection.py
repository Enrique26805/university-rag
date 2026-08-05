from qdrant_client.models import VectorParams, Distance

from vector_db.qdrant_store import (
    create_client,
    COLLECTION_NAME
)

client = create_client()

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

client.close()
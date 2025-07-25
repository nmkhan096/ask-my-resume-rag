# Load JSON chunks into Qdrant
#  only run ONCE to ingest data

import argparse
import json
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from rag_pipeline.config import qd_client, collection_name, EMBEDDING_MODEL, EMBEDDING_DIM

# Constants
# EMBEDDING_DIM = 512
# DEFAULT_MODEL = "jinaai/jina-embeddings-v2-small-en"
# collection = collection_name #"resume-rag"

# Initialize client (assuming local persistent Qdrant)
# qd_client = QdrantClient("http://localhost:6333")


def load_documents(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def setup_collection(collection_name):
    if not qd_client.collection_exists(collection_name):
        qd_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIM,
                distance=models.Distance.COSINE
            )
        )


def ingest_documents(docs, collection_name, model_handle):
    points = []
    for doc in docs:
        point = models.PointStruct(
            id=doc["id"],
            vector=models.Document(text=doc["text"], model=model_handle),
            payload={
                "text": doc["text"],
                "section": doc["metadata"]["section"]
            }
        )
        points.append(point)

    qd_client.upsert(collection_name=collection_name, points=points)


def create_section_index(collection_name):
    qd_client.create_payload_index(
        collection_name=collection_name,
        field_name="section",
        field_schema="keyword"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up Qdrant with parsed resume chunks.")
    parser.add_argument("--input", type=str, required=True, help="Path to parsed resume chunks JSON")
    #parser.add_argument("--collection", type=str, default="resume-rag", help="Name of the Qdrant collection")
    #parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Embedding model to use")
    
    args = parser.parse_args()

    docs = load_documents(args.input)
    setup_collection(collection_name)
    ingest_documents(docs, collection_name, EMBEDDING_MODEL)
    create_section_index(collection_name)

    print(f"Qdrant collection '{collection_name}' setup completed with {len(docs)} documents.")


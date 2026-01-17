from injector import inject
from dataclasses import dataclass
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
import weaviate
from weaviate import WeaviateClient
from weaviate.collections import Collection
from .embedding_service import EmbeddingsService
import os

COLLECTION_NAME = "Dataset"


@inject
class VectorDatabaseService:
    client: WeaviateClient
    vector_store: WeaviateVectorStore
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_service: EmbeddingsService):
        self.embeddings_service = embeddings_service
        self.client = weaviate.connect_to_custom(
            skip_init_checks=False,
            http_host=os.getenv("WEAVIATE_HTTP_HOST", "localhost"),
            http_port=int(os.getenv("WEAVIATE_HTTP_PORT", 8080)),
            http_secure=False,
            grpc_host=os.getenv("WEAVIATE_GRPC_HOST", "localhost"),
            grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", 50051)),
            grpc_secure=False
        )
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=self.embeddings_service.embeddings,
        )

    def get_retriver(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        return "\n\n".join([doc.page_content for doc in documents])

    @property
    def collection(self) -> Collection:
        return self.client.collections.get(COLLECTION_NAME)

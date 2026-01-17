from injector import inject
from dataclasses import dataclass
from langchain_community.storage import RedisStore
from langchain_core.embeddings import Embeddings
from langchain_classic.embeddings import CacheBackedEmbeddings
import redis
import tiktoken
from langchain_huggingface import HuggingFaceEmbeddings
import os


@inject
@dataclass
class EmbeddingsService:
    _store: RedisStore
    _embeddings: Embeddings
    _cache_backed_embeddings: CacheBackedEmbeddings

    def __init__(self, redis_client: redis.Redis):
        self._store = RedisStore(client=redis_client)
        self._embeddings = HuggingFaceEmbeddings(
            model_name="Qwen/Qwen3-Embedding-0.6B",
            cache_folder=os.path.join(
                os.getcwd(), "internal", "core", "embeddings"),
            model_kwargs={
                "trust_remote_code": True,
                "device": "cpu"  # Force CPU usage to avoid CUDA memory issues
            }
        )
        # self._embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self._cache_backed_embeddings = CacheBackedEmbeddings.from_bytes_store(
            self._store, self._embeddings, namespace="embeddings")

    @classmethod
    def calculate_token_count(cls, query: str) -> int:
        '''计算传入文本的token数'''
        encoding = tiktoken.encoding_for_model("gpt-5")
        return len(encoding.encode(query))

    @property
    def store(self) -> RedisStore:
        return self._store

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    @property
    def cache_backed_embeddings(self) -> CacheBackedEmbeddings:
        return self._cache_backed_embeddings

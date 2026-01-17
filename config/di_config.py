# config/di_config.py
import redis
import redis.asyncio as async_redis
from injector import Module, provider, singleton, Injector

from config.config import REDIS_CONFIG
from internal.service.indexing_service import IndexingService
from internal.service.process_rule_service import ProcessRuleService
from internal.service.embedding_service import EmbeddingsService
from internal.service.jieba_service import JiebaService
from internal.service.keyword_table_service import KeywordTableService
from internal.service.vector_database_service import VectorDatabaseService
from internal.service.upload_file_service import UploadFileService
from internal.service.cos_service import CosService
from internal.core.file_extractor import FileExtractor


class RedisModule(Module):
    @singleton
    @provider
    def provide_async_redis(self) -> async_redis.Redis:
        return async_redis.Redis(connection_pool=async_redis.ConnectionPool.from_url(**REDIS_CONFIG))

    @singleton
    @provider
    def provide_sync_redis(self) -> redis.Redis:
        return redis.Redis.from_url(**REDIS_CONFIG)


class ServiceModule(Module):
    @singleton
    @provider
    def provide_upload_file_service(self) -> UploadFileService:
        return UploadFileService()

    @singleton
    @provider
    def provide_cos_service(self, upload_file_service: UploadFileService) -> CosService:
        return CosService(upload_file_service)

    @singleton
    @provider
    def provide_embeddings_service(self, redis_client: redis.Redis) -> EmbeddingsService:
        return EmbeddingsService(redis_client)

    @singleton
    @provider
    def provide_vector_database_service(self, embeddings_service: EmbeddingsService) -> VectorDatabaseService:
        return VectorDatabaseService(embeddings_service)

    @singleton
    @provider
    def provide_jieba_service(self) -> JiebaService:
        return JiebaService()

    @singleton
    @provider
    def provide_keyword_table_service(self) -> KeywordTableService:
        return KeywordTableService()

    @singleton
    @provider
    def provide_process_rule_service(self) -> ProcessRuleService:
        return ProcessRuleService()

    @singleton
    @provider
    def provide_file_extractor(self, cos_service: CosService) -> FileExtractor:
        return FileExtractor(cos_service)

    @singleton
    @provider
    def provide_indexing_service(
        self,
        file_extractor: FileExtractor,
        process_rule_service: ProcessRuleService,
        embeddings_service: EmbeddingsService,
        jieba_service: JiebaService,
        keyword_table_service: KeywordTableService,
        vector_database_service: VectorDatabaseService
    ) -> IndexingService:
        return IndexingService(
            file_extractor=file_extractor,
            process_rule_service=process_rule_service,
            embeddings_service=embeddings_service,
            jieba_service=jieba_service,
            keyword_table_service=keyword_table_service,
            vector_database_service=vector_database_service
        )


injector = Injector([RedisModule(), ServiceModule()])

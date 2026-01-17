from uuid import UUID
from celery import shared_task
from config.logger import get_logger

logger = get_logger(__name__)


@shared_task
def build_documents(document_ids: list[UUID]):
    """根据传递的文档ID列表构建文档"""
    import asyncio

    async def _build_documents_async():
        try:
            logger.info(f"build_documents started: {document_ids}")

            logger.info("Initializing database connection")
            from tortoise import Tortoise
            from config.config import DB_CONFIG
            await Tortoise.init(config=DB_CONFIG)
            logger.info("Database initialized successfully")

            logger.info("get indexing_service")
            from config.di_config import injector
            from internal.service import IndexingService
            indexing_service = injector.get(IndexingService)
            logger.info("indexing_service initialized successfully")

            await indexing_service.build_documents(document_ids)

        except Exception as e:
            logger.exception(f"Error in build_documents task: {e}")
            raise
        finally:
            logger.info("Step 15: Closing database connections")
            await Tortoise.close_connections()

    # Run the async function
    return asyncio.run(_build_documents_async())


# @shared_task
# def build_documents(document_ids: list[UUID]):

#     def
#     from config.di_config import injector
#     from internal.service import IndexingService
#     import asyncio

#     indexing_service = injector.get(IndexingService)
#     return asyncio.run(indexing_service.build_documents(document_ids))

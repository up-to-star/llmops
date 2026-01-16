from uuid import UUID
from celery import shared_task
from config.config import celery_app

@shared_task
def build_documents(document_ids: list[UUID]):
    """根据传递的文档ID列表构建文档"""
    from app.http.module import injector
    from internal.service import IndexingService

    indexing_service = injector.get(IndexingService)
    indexing_service.build_documents(document_ids)
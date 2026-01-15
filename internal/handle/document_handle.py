from injector import inject
from dataclasses import dataclass
from uuid import UUID
from internal.schema import CreateDocumentRequest, CreateDocumentResponse
from pkg.response import Response
from internal.service import DocumentService


@inject
@dataclass
class DocumentHandler:
    """文档处理类"""
    document_service: DocumentService

    async def create_documents(self, dataset_id: UUID, request: CreateDocumentRequest):
        documents, batch = await self.document_service.create_documents(dataset_id, request.upload_file_ids, request.process_type, request.rule)
        return Response(
            data=CreateDocumentResponse(documents=documents, batch=batch)
        )

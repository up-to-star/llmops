from injector import inject
from dataclasses import dataclass
from uuid import UUID
from internal.schema import (CreateDatasetRequest, GetDatasetResponse,
                             UpdateDatasetRequest, GetDatasetWithPageResponse, GetDatasetWithPageRequest)
from internal.service import DatasetService, EmbeddingsService, JiebaService
from pkg.response import Response
from pkg.paginator import PageModel
from internal.core.file_extractor import FileExtractor
from internal.model import UploadFile


@inject
@dataclass
class DatasetHandler:
    dataset_service: DatasetService
    embeddings_service: EmbeddingsService
    jieba_service: JiebaService
    file_extractor: FileExtractor

    async def embeddings_query(self, query: str):
        # keywords = self.jieba_service.extract_keywords(query)
        # return Response(
        #     message=f"Embeddings for {query} retrieved successfully",
        #     data=keywords
        # )
        upload_file = await UploadFile.filter(id="ef890894-1738-40fb-b660-b95a3f2d486b").first()
        print(upload_file)
        content = await self.file_extractor.load(upload_file, True, False)
        return Response(
            message=f"Embeddings for {query} retrieved successfully",
            data=content
        )

    async def create_dataset(self, request: CreateDatasetRequest):
        dataset = await self.dataset_service.create_dataset(request)
        return Response(
            message=f"Dataset {dataset.name} created successfully"
        )

    async def get_dataset(self, dataset_id: UUID):
        dataset = await self.dataset_service.get_dataset(dataset_id)
        document_count = await self.dataset_service.get_document_count(dataset_id)
        hit_count = await self.dataset_service.get_hit_count(dataset_id)
        character_count = await self.dataset_service.get_character_count(dataset_id)
        related_app_count = await self.dataset_service.get_related_app_count(dataset_id)
        print(hit_count)
        return Response(
            message=f"Dataset {dataset.name} retrieved successfully",
            data=GetDatasetResponse(
                id=str(dataset.id),
                name=dataset.name,
                icon=dataset.icon,
                description=dataset.description,
                document_count=document_count,
                hit_count=hit_count,
                related_app_count=related_app_count,
                character_count=character_count,
                created_at=int(dataset.created_at.timestamp()),
                update_at=int(dataset.update_at.timestamp())
            )
        )

    async def update_dataset(self, dataset_id: UUID, request: UpdateDatasetRequest):
        await self.dataset_service.update_dataset(dataset_id, request)
        return Response(
            message=f"Dataset {request.name} updated successfully"
        )

    async def get_datasets_with_page(self, request: GetDatasetWithPageRequest):
        datasets, paginator = await self.dataset_service.get_datasets_with_page(request)
        response_list = []
        for dataset in datasets:
            document_count = await self.dataset_service.get_document_count(dataset.id)
            character_count = await self.dataset_service.get_character_count(dataset.id)
            related_app_count = await self.dataset_service.get_related_app_count(dataset.id)
            response = GetDatasetWithPageResponse(
                id=str(dataset.id),
                name=dataset.name,
                icon=dataset.icon,
                description=dataset.description,
                document_count=document_count,
                character_count=character_count,
                related_app_count=related_app_count,
                created_at=int(dataset.created_at.timestamp()),
                update_at=int(dataset.update_at.timestamp())
            )
            response_list.append(response)
        return Response(
            message=f"Datasets retrieved successfully",
            data=PageModel(
                data=response_list,
                paginator=paginator
            )
        )

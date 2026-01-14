from injector import inject
from dataclasses import dataclass
from internal.schema import CreateDatasetRequest, GetDatasetWithPageRequest
from internal.model import Dataset, Document, Segment, AppDatasetJoin
from internal.exception import ValidationException, NotFoundException
from internal.entity.dataset_entity import DEFAULT_DATASET_DESCRIPTION
from uuid import UUID
from tortoise.functions import Sum
from config.logger import get_logger
from pkg.paginator import Paginator, BaseQuery

logger = get_logger(__name__)


@inject
@dataclass
class DatasetService:

    async def get_datasets_with_page(self, request: GetDatasetWithPageRequest) -> tuple[list[Dataset], Paginator]:
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        filter = Dataset.filter(account_id=account_id)
        if request.search_word:
            filter = filter.filter(name__icontains=request.search_word)
        query = BaseQuery(Dataset, request.current_page, request.page_size)
        datasets, paginator = await query.paginate(filter)
        return datasets, paginator
    

    async def update_dataset(self, dataset_id: UUID, request: CreateDatasetRequest):
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        dataset = await Dataset.get_or_none(account_id=account_id, id=dataset_id)
        if not dataset:
            raise NotFoundException(
                f"Dataset with id {dataset_id} does not exist")

        check_dataset = await Dataset.filter(account_id=account_id, name=request.name).exclude(id=dataset_id).first()
        if check_dataset:
            raise ValidationException(
                f"Dataset with name {request.name} already exists")

        if request.description is None or request.description.strip() == "":
            request.description = DEFAULT_DATASET_DESCRIPTION.format(
                name=request.name)

        logger.info(f"Updating dataset {dataset_id} with {request}")
        dataset.name = request.name
        dataset.icon = request.icon
        dataset.description = request.description
        await dataset.save()

    async def create_dataset(self, request: CreateDatasetRequest) -> Dataset:
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        dataset = await Dataset.filter(account_id=account_id, name=request.name).first()
        if dataset:
            raise ValidationException(
                f"Dataset with name {request.name} already exists")

        if request.description is None or request.description.strip() == "":
            request.description = DEFAULT_DATASET_DESCRIPTION.format(
                name=request.name)

        dataset = Dataset(
            account_id=account_id,
            name=request.name,
            icon=request.icon,
            description=request.description
        )
        await dataset.save()
        return dataset

    async def get_dataset(self, dataset_id: UUID) -> Dataset:
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        dataset = await Dataset.get_or_none(account_id=account_id, id=dataset_id)
        if not dataset:
            raise NotFoundException(
                f"Dataset with id {dataset_id} does not exist")
        return dataset

    async def get_document_count(self, dataset_id: UUID) -> int:
        document_count = await Document.filter(dataset_id=dataset_id).count()
        return document_count

    async def get_hit_count(self, dataset_id: UUID) -> int:
        hit_count_result = await Segment.filter(dataset_id=dataset_id).annotate(
            total_hits=Sum('hit_count')
        ).values('total_hits')
        hit_count = hit_count_result[0]['total_hits'] if hit_count_result and hit_count_result[0].get(
            'total_hits') else 0
        return hit_count

    async def get_character_count(self, dataset_id: UUID) -> int:
        character_count = await Document.filter(dataset_id=dataset_id).annotate(
            total_characters=Sum('character_count')
        ).values('total_characters')
        character_count = character_count[0]['total_characters'] if character_count and character_count[0].get(
            'total_characters') else 0
        return character_count

    async def get_related_app_count(self, dataset_id: UUID) -> int:
        related_app_count = await AppDatasetJoin.filter(dataset_id=dataset_id).count()
        return related_app_count

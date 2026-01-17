from injector import inject
from dataclasses import dataclass
from internal.entity.dataset_entity import ProcessType
from internal.entity.upload_file_entity import ALLOWED_FILE_EXTENSIONS
from uuid import UUID
from internal.model import Document, Dataset, UploadFile, ProcessRule
from internal.exception import ForbiddenException, FailException
from config.logger import get_logger
import time
import random
from internal.tasks.document_task import build_documents

logger = get_logger(__name__)


@inject
@dataclass
class DocumentService:
    """文档服务类"""

    async def create_documents(self, dataset_id: UUID,
                               upload_file_ids: list[UUID], process_type: ProcessType = ProcessType.AUTOMATIC,
                               rule: dict = None) -> tuple[list[Document], str]:
        """创建文档"""
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        dataset = await Dataset.filter(id=dataset_id).first()
        if not dataset or str(dataset.account_id) != account_id:
            raise ForbiddenException(
                f"Dataset with id {dataset_id} not found or not belong to the account")
        upload_files = await UploadFile.filter(account_id=account_id, id__in=upload_file_ids).all()
        if upload_files:
            upload_files = [
                upload_file for upload_file in upload_files if upload_file.extension in ALLOWED_FILE_EXTENSIONS]
        if len(upload_files) == 0:
            logger.warning(
                f"上传文档列表未解析到合法文件，account_id: {account_id}, dataset_id: {dataset_id}, upload_file_ids: {upload_file_ids}")
            raise FailException(
                f"未解析到合法文件，请重新上传")
        batch = time.strftime("%Y%m%d%H%M%S") + \
            str(random.randint(100000, 999999))
        process_rule = await ProcessRule.create(
            account_id=account_id,
            dataset_id=dataset_id,
            mode=process_type,
            rule=rule,
        )
        position = await self.get_latest_document_position(dataset_id)
        documents = []
        for upload_file in upload_files:
            position += 1
            document = await Document.create(
                account_id=account_id,
                dataset_id=dataset_id,
                upload_file_id=upload_file.id,
                process_rule_id=process_rule.id,
                batch=batch,
                name=upload_file.name,
                position=position,
            )
            documents.append(document)
        # 异步构建文档索引
        build_documents.delay([document.id for document in documents])

        return documents, batch

    async def get_latest_document_position(self, dataset_id: UUID) -> int:
        """获取最新文档位置"""
        latest_document = await Document.filter(dataset_id=dataset_id).order_by("-position").first()
        return latest_document.position if latest_document else 0

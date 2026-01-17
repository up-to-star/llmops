from injector import inject
from dataclasses import dataclass
from uuid import UUID
from internal.model import Document, UploadFile, ProcessRule, Segment
from config.logger import get_logger
from datetime import datetime
from internal.entity.dataset_entity import DocumentStatus, SegmentStatus
from langchain_core.documents import Document as LCDocument
from internal.core.file_extractor import FileExtractor
from .process_rule_service import ProcessRuleService
import re
from .embedding_service import EmbeddingsService
from .jieba_service import JiebaService
from .keyword_table_service import KeywordTableService
from .vector_database_service import VectorDatabaseService
import uuid
from internal.utils.helper import generate_text_hash

logger = get_logger(__name__)


@inject
@dataclass
class IndexingService:
    """索引服务"""
    file_extractor: FileExtractor
    process_rule_service: ProcessRuleService
    embeddings_service: EmbeddingsService
    jieba_service: JiebaService
    keyword_table_service: KeywordTableService
    vector_database_service: VectorDatabaseService

    async def build_documents(self, document_ids: list[UUID]):
        """根据传递的文档ID列表构建文档, 涵盖加载、分割、索引构建、数据存储等"""
        # 根据传递的文档id获取所有文档
        documents: list[Document] = await Document.filter(id__in=document_ids).all()
        logger.info(f"开始构建文档索引，文档数量: {len(documents)}")

        for document in documents:
            try:
                document.status = DocumentStatus.PARSING
                document.process_started_at = datetime.now()
                await document.save()

                lc_documents = await self._parsing(document)
                lc_segments = await self._splitting(document, lc_documents)
                await self._indexing(document, lc_segments)
                await self._completed(document, lc_segments)
                logger.info(f"文档索引构建完成，文档ID列表: {document_ids}")

            except Exception as e:
                logger.exception(
                    f"构建文档索引失败，document_id: {document.id}, error: {e}")
                document.status = DocumentStatus.ERROR
                document.error = str(e)
                document.stopped_at = datetime.now()
                await document.save()

    async def _completed(self, document: Document, lc_segments: list[LCDocument]) -> None:
        """文档索引构建完成"""

        for lc_segment in lc_segments:
            lc_segment.metadata['document_enabled'] = True
            lc_segment.metadata['segment_enabled'] = True

        for i in range(0, len(lc_segments), 10):
            chunks = lc_segments[i:i+10]
            ids = [chunk.metadata['node_id'] for chunk in chunks]

            self.vector_database_service.vector_store.add_documents(
                chunks, ids=ids)

            segments = await Segment.filter(node_id__in=ids).all()
            for segment in segments:
                segment.status = SegmentStatus.COMPLETED
                segment.completed = datetime.now()
                segment.enabled = True
                await segment.save()
        document.status = DocumentStatus.COMPLETED
        document.completed_at = datetime.now()
        document.enabled = True
        await document.save()

    async def _parsing(self, document: Document) -> list[LCDocument]:
        """解析文档"""
        upload_file = await UploadFile.get_or_none(id=document.upload_file_id)
        if not upload_file:
            raise ValueError(
                f"Upload file not found for document {document.id}")

        lc_documents: list[LCDocument] = await self.file_extractor.load(
            upload_file, False, True)

        if not lc_documents:
            logger.warning(
                f"No documents extracted from file {upload_file.key}")
            lc_documents = []

        # Filter out documents with None page_content and clean the text
        valid_documents = []
        for lc_document in lc_documents:
            if lc_document and hasattr(lc_document, 'page_content') and lc_document.page_content is not None:
                try:
                    cleaned_content = self._clean_extra_text(
                        lc_document.page_content)
                    if cleaned_content is not None:
                        lc_document.page_content = cleaned_content
                        valid_documents.append(lc_document)
                    else:
                        logger.warning(f"Cleaned content is None for document")
                except Exception as e:
                    logger.warning(f"Error cleaning document content: {e}")
            else:
                logger.warning(f"Skipping invalid document: {lc_document}")

        lc_documents = valid_documents

        document.status = DocumentStatus.SPLITTING
        document.parsing_completed_at = datetime.now()

        # Safe character count calculation
        total_chars = 0
        for lc_document in lc_documents:
            if lc_document and hasattr(lc_document, 'page_content') and lc_document.page_content is not None:
                total_chars += len(lc_document.page_content)

        document.character_count = total_chars
        await document.save()
        return lc_documents

    async def _splitting(self, document: Document, lc_documents: list[LCDocument]) -> list[LCDocument]:
        """分割文档"""
        process_rule = await ProcessRule.get_or_none(id=document.process_rule_id)
        text_splitter = self.process_rule_service.get_text_splitter_by_process_rule(
            process_rule, self.embeddings_service.calculate_token_count)
        for lc_document in lc_documents:
            lc_document.page_content = self.process_rule_service.clean_text_by_process_rule(
                process_rule, lc_document.page_content)
        lc_segments = text_splitter.split_documents(lc_documents)
        latest_segment = await Segment.filter(
            document_id=document.id).order_by("-position").first()
        position = latest_segment.position if latest_segment else 0
        segments = []
        for lc_segment in lc_segments:
            position += 1
            segment = Segment(
                account_id=document.account_id,
                dataset_id=document.dataset_id,
                document_id=document.id,
                node_id=uuid.uuid4(),
                position=position,
                content=lc_segment.page_content,
                character_count=len(lc_segment.page_content),
                token_count=self.embeddings_service.calculate_token_count(
                    lc_segment.page_content),
                hash=generate_text_hash(lc_segment.page_content),
                status=SegmentStatus.WAITING,
                keywords={},
            )
            await segment.save()
            lc_segment.metadata = {
                "account_id": str(document.account_id),
                "dataset_id": str(document.dataset_id),
                "document_id": str(document.id),
                "segment_id": str(segment.id),
                "node_id": str(segment.node_id),
                "document_enabled": False,
                "segment_enabled": False,
            }
            segments.append(segment)
        document.token_count = sum(
            segment.token_count for segment in segments)
        document.status = DocumentStatus.INDEXING
        document.splitting_completed_at = datetime.now()
        await document.save()
        return lc_segments

    async def _indexing(self, document: Document, lc_segments: list[LCDocument]) -> None:
        """索引文档"""
        for lc_segment in lc_segments:
            keywords = self.jieba_service.extract_keywords(
                lc_segment.page_content, 10)
            segment: Segment = await Segment.filter(
                id=lc_segment.metadata["segment_id"]
            ).first()
            segment.keywords = keywords
            segment.status = SegmentStatus.INDEXING
            segment.indexing_completed_at = datetime.now()
            await segment.save()

            keyword_table_record = await self.keyword_table_service.get_keyword_table_from_dataset_id(
                document.dataset_id)
            keyword_table = {
                field: set(val)
                for field, val in keyword_table_record.keyword_table.items()
            }
            for keyword in keywords:
                if keyword not in keyword_table:
                    keyword_table[keyword] = set()
                keyword_table[keyword].add(segment.id)
            keyword_table_record.keyword_table = {
                field: list(val) for field, val in keyword_table.items()
            }
            await keyword_table_record.save()

        document.indexing_completed_at = datetime.now()
        await document.save()

    @classmethod
    def _clean_extra_text(cls, text: str) -> str:
        """清理文本中的额外空文本"""
        if text is None:
            return ""
        text = re.sub(r"<\|", "<", text)
        text = re.sub(r"\|>", ">", text)
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E\-\x1F\x7F\xEF\xBF\xBE]", "", text)
        text = re.sub("\uFFFE", "", text)
        return text

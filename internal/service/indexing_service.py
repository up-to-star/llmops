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

    def build_documents(self, document_ids: list[UUID]):
        """根据传递的文档ID列表构建文档, 涵盖加载、分割、索引构建、数据存储等"""
        # 根据传递的文档id获取所有文档
        documents: list[Document] = Document.filter(id__in=document_ids).all()

        for document in documents:
            try:
                document.status = DocumentStatus.PARSING
                document.process_started_at = datetime.now()
                document.save()

                lc_documents = self._parsing(document)
                lc_segments = self._splitting(document, lc_documents)
                self._indexing(document, lc_segments)

            except Exception as e:
                logger.exception(
                    f"构建文档索引失败，document_id: {document.id}, error: {e}")
                document.status = DocumentStatus.ERROR
                document.error = str(e)
                document.stopped_at = datetime.now()
                document.save()

    def _parsing(self, document: Document) -> list[LCDocument]:
        """解析文档"""
        upload_file = UploadFile.get_or_none(id=document.upload_file_id)
        lc_documents: list[LCDocument] = self.file_extractor.load(
            upload_file, False, True)

        for lc_document in lc_documents:
            lc_document.page_content = self._clean_extra_text(
                lc_document.page_content)
        document.status = DocumentStatus.SPLITTING
        document.parsing_completed_at = datetime.now()
        document.character_count = sum(
            len(lc_document.page_content) for lc_document in lc_documents)
        document.save()
        return lc_documents

    def _splitting(self, document: Document, lc_documents: list[LCDocument]) -> list[LCDocument]:
        """分割文档"""
        process_rule = ProcessRule.get_or_none(id=document.process_rule_id)
        text_splitter = self.process_rule_service.get_text_splitter_by_process_rule(
            process_rule, self.embeddings_service.calculate_token_count)
        for lc_document in lc_documents:
            lc_document.page_content = self.process_rule_service.clean_text_by_process_rule(
                process_rule, lc_document.page_content)
        lc_segments = text_splitter.split_documents(lc_documents)
        latest_segment = Segment.filter(
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
            )
            segment.save()
            lc_segment.metadata = {
                "account_id": str(document.account_id),
                "dataset_id": str(document.dataset_id),
                "document_id": str(document.id),
                "segment_id": str(segment.id),
                "node": str(segment.node_id),
                "document_enabled": False,
                "segment_enabled": False,
            }
            segments.append(segment)
        document.token_count = sum(
            segment.token_count for segment in segments)
        document.status = DocumentStatus.INDEXING
        document.splitting_completed_at = datetime.now()
        document.save()
        return lc_segments

    def _indexing(self, document: Document, lc_segments: list[LCDocument]) -> None:
        """索引文档"""
        for lc_segment in lc_segments:
            keywords = self.jieba_service.extract_keywords(
                lc_segment.page_content, 10)
            segment = Segment.filter(
                id=lc_segment.metadata["segment_id"]
            ).first()
            segment.keywords = keywords
            segment.status = SegmentStatus.INDEXING
            segment.indexing_completed_at = datetime.now()
            segment.save()
            
        document.status = DocumentStatus.INDEXED
        document.indexing_completed_at = datetime.now()
        document.save()

    @classmethod
    def _clean_extra_text(cls, text: str) -> str:
        """清理文本中的额外空文本"""
        text = re.sub(r"<\|", "<", text)
        text = re.sub(r"\|>", ">", text)
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E\-\x1F\x7F\xEF\xBF\xBE]", "", text)
        text = re.sub("\uFFFE", "", text)

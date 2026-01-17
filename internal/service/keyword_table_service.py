from injector import inject
from dataclasses import dataclass
from uuid import UUID
from internal.model import KeywordTable


@inject
@dataclass
class KeywordTableService:
    '''知识库关键词表服务'''

    async def get_keyword_table_from_dataset_id(self, dataset_id: UUID) -> KeywordTable:
        '''根据数据集id获取知识库关键词表'''
        keyword_table = await KeywordTable.get_or_none(dataset_id=dataset_id)
        if not keyword_table:
            keyword_table = KeywordTable(
                dataset_id=dataset_id,
                keyword_table={}
            )
            await keyword_table.save()
        return keyword_table

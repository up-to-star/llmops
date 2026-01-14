from injector import inject
from dataclasses import dataclass
from internal.entity.jieba_entity import STOPWORD_SET
from jieba.analyse import default_tfidf
from jieba import analyse


@inject
@dataclass
class JiebaService:

    def __init__(self):
        default_tfidf.stop_words = STOPWORD_SET

    @classmethod
    def extract_keywords(cls, text: str, max_keword_pre_chunk: int = 10) -> list[str]:
        """根据输入文本，提取对应文本的关键词列表"""
        return analyse.extract_tags(
            sentence=text,
            topK=max_keword_pre_chunk,
        )

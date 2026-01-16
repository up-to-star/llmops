from injector import inject
from dataclasses import dataclass
from internal.model import ProcessRule
from typing import Callable, Optional
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter
import re


@inject
@dataclass
class ProcessRuleService:
    """处理规则服务"""

    @classmethod
    def get_text_splitter_by_process_rule(cls, process_rule: ProcessRule, length_function: Callable[[str], int] = len, **kwargs) -> TextSplitter:
        """根据处理规则获取文本分割器"""
        return RecursiveCharacterTextSplitter(
            chunk_size=process_rule.rule['segment']['chunk_size'],
            chunk_overlap=process_rule.rule['segment']['chunk_overlap'],
            separators=process_rule.rule['segment']['separators'],
            is_separator_regex=True,
            length_function=length_function,
            **kwargs
        )

    @classmethod
    def clean_text_by_process_rule(cls, process_rule: ProcessRule, text: str) -> str:
        """根据处理规则清理文本"""
        for pre_process_rule in process_rule.rule['pre_process_rules']:
            if pre_process_rule['id'] == 'remove_extra_space' and pre_process_rule['enabled'] is True:
                pattern = r"\n{3,}"
                text = re.sub(pattern, "\n\n", text)
                pattern = fr"[\t\f\r\x20\u00a0\u180e\u2000-\u200a\u202f\u205f\u3000]{2, }"
                text = re.sub(pattern, " ", text)
            if pre_process_rule['id'] == 'remove_url_and_email' and pre_process_rule['enabled'] is True:
                pattern = r"https?://[^\s,。！？；：,.!?;:]+|\b[\w\.-]+@[\w\.-]+\.\w+\b"
                text = re.sub(pattern, "", text)
                return text

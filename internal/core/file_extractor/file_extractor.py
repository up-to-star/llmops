from pathlib import Path
from injector import inject
from dataclasses import dataclass
from internal.service import CosService
from internal.model import UploadFile
from typing import Union
from langchain_core.documents import Document as LCDocument
import tempfile
import os
from langchain_community.document_loaders import (
    UnstructuredExcelLoader, UnstructuredPDFLoader,
    UnstructuredHTMLLoader, UnstructuredCSVLoader,
    UnstructuredMarkdownLoader, UnstructuredPowerPointLoader,
    UnstructuredXMLLoader, UnstructuredFileLoader, TextLoader)

import requests


@inject
@dataclass
class FileExtractor:
    """
    Extracts files from a given path.
    """
    cos_service: CosService

    async def load(self, upload_file: UploadFile, return_text: bool = False, is_unstructured: bool = False) -> Union[list[LCDocument], str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(
                temp_dir, os.path.basename(upload_file.key))
            await self.cos_service.download_file(upload_file.key, file_path)

            return self.load_from_file(file_path, return_text, is_unstructured)

    @classmethod
    def load_from_file(cls, file_path: str, return_text: bool = False, is_unstructured: bool = True) -> Union[list[LCDocument], str]:
        """
        Loads a file from the given path.
        """
        delimiter = "\n\n"
        file_extension = Path(file_path).suffix.lower()

        loader = None
        if file_extension in [".xlsx", ".xls"]:
            loader = UnstructuredExcelLoader(file_path)
        elif file_extension == '.pdf':
            loader = UnstructuredPDFLoader(file_path)
        elif file_extension in [".md", ".markdown"]:
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_extension in [".html", ".htm"]:
            loader = UnstructuredHTMLLoader(file_path)
        elif file_extension == '.csv':
            loader = UnstructuredCSVLoader(file_path)
        elif file_extension in [".pptx", ".ppt"]:
            loader = UnstructuredPowerPointLoader(file_path)
        elif file_extension == '.xml':
            loader = UnstructuredXMLLoader(file_path)
        else:
            loader = UnstructuredFileLoader(
                file_path) if is_unstructured else TextLoader(file_path)

        return delimiter.join([doc.page_content for doc in loader.load()]) if return_text else loader.load()

    @classmethod
    def load_from_url(cls, url: str, return_text: bool = False) -> Union[list[LCDocument], str]:
        """
        Loads a file from the given url.
        """
        response = requests.get(url)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, os.path.basename(url))
            with open(file_path, "wb") as f:
                f.write(response.content)
            return cls.load_from_file(file_path, return_text)

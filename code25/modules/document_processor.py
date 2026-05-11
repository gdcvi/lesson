"""文档处理模块"""
import os
from typing import List, Optional
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
)
try:
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    HAS_UNSTRUCTURED = True
except ImportError:
    HAS_UNSTRUCTURED = False
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.settings import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP


class DocumentProcessor:
    """文档处理类"""

    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE,
                 chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )

    def load_document(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif ext == '.docx':
                loader = Docx2txtLoader(file_path)
            elif ext == '.md':
                loader = UnstructuredMarkdownLoader(file_path)
            elif ext == '.csv':
                loader = CSVLoader(file_path, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                return self._load_excel(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
            return loader.load()
        except Exception as e:
            raise Exception(f"加载文档失败 {file_path}: {str(e)}")

    def _load_excel(self, file_path: str) -> List[Document]:
        try:
            import pandas as pd
            excel_file = pd.ExcelFile(file_path)
            documents = []
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                text = df.to_string(index=False)
                doc = Document(
                    page_content=text,
                    metadata={"source": file_path, "sheet": sheet_name}
                )
                documents.append(doc)
            return documents
        except Exception as e:
            raise Exception(f"加载Excel文件失败: {str(e)}")

    def split_documents(self, docs: List[Document]) -> List[Document]:
        return self.text_splitter.split_documents(docs)

    def process_uploaded_files(self, uploaded_files, temp_dir: str,
                               persistent: bool = False) -> tuple:
        saved_files = []
        all_documents = []
        for idx, uploaded_file in enumerate(uploaded_files, 1):
            try:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                os.makedirs(temp_dir, exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    continue
                saved_files.append(file_path)
                docs = self.load_document(file_path)
                if not docs:
                    continue
                for doc in docs:
                    doc.metadata["persistent"] = persistent
                    doc.metadata["filename"] = uploaded_file.name
                split_docs = self.split_documents(docs)
                all_documents.extend(split_docs)
            except Exception as e:
                print(f"处理上传文件失败 {uploaded_file.name}: {e}")
                continue
        return all_documents, saved_files

    def cleanup_temp_files(self, file_paths: List[str]):
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"删除临时文件失败 {file_path}: {e}")

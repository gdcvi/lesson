"""向量存储管理模块"""
import os
import json
from typing import List, Optional, Dict
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from config.settings import (
    CHROMA_DB_PATH,
    EMBEDDING_MODEL,
    DASHSCOPE_API_KEY,
    DEFAULT_TOP_K
)


class VectorStoreManager:
    """向量存储管理类"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or CHROMA_DB_PATH
        self.embeddings = DashScopeEmbeddings(
            model=EMBEDDING_MODEL,
            dashscope_api_key=DASHSCOPE_API_KEY
        )
        self.collections_metadata_file = os.path.join(self.db_path, "collections_metadata.json")
        os.makedirs(self.db_path, exist_ok=True)

    def _get_collection_path(self, collection_name: str) -> str:
        return os.path.join(self.db_path, collection_name)

    def _validate_and_convert_name(self, name: str) -> str:
        import re
        if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{1,510}[a-zA-Z0-9]$', name):
            return name
        valid_name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
        if not re.match(r'^[a-zA-Z0-9]', valid_name):
            valid_name = 'kb_' + valid_name
        if not re.match(r'.*[a-zA-Z0-9]$', valid_name):
            valid_name = valid_name.rstrip('._-') + '_kb'
        if len(valid_name) < 3:
            valid_name = valid_name + '_kb'
        elif len(valid_name) > 512:
            valid_name = valid_name[:512].rstrip('._-')
            if len(valid_name) < 3:
                valid_name = valid_name + 'kb'
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{1,510}[a-zA-Z0-9]$', valid_name):
            import hashlib
            hash_name = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
            valid_name = f'kb_{hash_name}'
        return valid_name

    def _load_collections_metadata(self) -> Dict:
        try:
            if os.path.exists(self.collections_metadata_file):
                with open(self.collections_metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载集合元数据失败: {e}")
        return {}

    def _save_collections_metadata(self, metadata: Dict):
        try:
            with open(self.collections_metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存集合元数据失败: {e}")

    def create_collection(self, collection_name: str, description: str = "") -> bool:
        try:
            valid_name = self._validate_and_convert_name(collection_name)
            collection_path = self._get_collection_path(valid_name)
            Chroma(
                collection_name=valid_name,
                embedding_function=self.embeddings,
                persist_directory=collection_path
            )
            metadata = self._load_collections_metadata()
            metadata[valid_name] = {
                "display_name": collection_name,
                "description": description,
                "created_at": "",
                "document_count": 0
            }
            self._save_collections_metadata(metadata)
            return True
        except Exception as e:
            print(f"创建集合失败: {e}")
            return False

    def get_collection(self, collection_name: str) -> Optional[Chroma]:
        try:
            collection_path = self._get_collection_path(collection_name)
            if not os.path.exists(collection_path):
                return None
            return Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=collection_path
            )
        except Exception as e:
            print(f"获取集合失败: {e}")
            return None

    def add_documents(self, collection_name: str, documents: List[Document]) -> bool:
        try:
            chroma_db = self.get_collection(collection_name)
            if chroma_db is None:
                raise Exception(f"集合 {collection_name} 不存在")
            chroma_db.add_documents(documents)
            metadata = self._load_collections_metadata()
            if collection_name in metadata:
                metadata[collection_name]["document_count"] = len(chroma_db.get()["ids"])
                self._save_collections_metadata(metadata)
            return True
        except Exception as e:
            print(f"添加文档失败: {e}")
            return False

    def delete_collection(self, collection_name: str) -> bool:
        try:
            import shutil
            collection_path = self._get_collection_path(collection_name)
            if not os.path.exists(collection_path):
                return False
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    shutil.rmtree(collection_path)
                    break
                except PermissionError:
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(1)
                    else:
                        raise
            metadata = self._load_collections_metadata()
            if collection_name in metadata:
                del metadata[collection_name]
                self._save_collections_metadata(metadata)
            return True
        except Exception as e:
            print(f"删除集合失败: {e}")
            return False

    def list_collections(self) -> List[Dict]:
        metadata = self._load_collections_metadata()
        collections = []
        for name, info in metadata.items():
            collections.append({
                "name": name,
                "display_name": info.get("display_name", name),
                "description": info.get("description", ""),
                "document_count": info.get("document_count", 0)
            })
        return collections

    def get_retriever(self, collection_name: str, k: int = DEFAULT_TOP_K):
        try:
            chroma_db = self.get_collection(collection_name)
            if chroma_db is None:
                return None
            return chroma_db.as_retriever(search_kwargs={"k": k})
        except Exception as e:
            print(f"获取检索器失败: {e}")
            return None

    def collection_exists(self, collection_name: str) -> bool:
        return os.path.exists(self._get_collection_path(collection_name))

    def get_collection_stats(self, collection_name: str) -> Dict:
        try:
            chroma_db = self.get_collection(collection_name)
            if chroma_db is None:
                return {"exists": False}
            data = chroma_db.get()
            return {"exists": True, "document_count": len(data["ids"]), "collection_name": collection_name}
        except Exception as e:
            print(f"获取集合统计信息失败: {e}")
            return {"exists": False, "error": str(e)}

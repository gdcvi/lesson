"""提示词管理模块"""
import json
import os
from typing import Dict, List, Optional
from config.settings import CHROMA_DB_PATH


class PromptManager:
    """提示词管理类"""

    def __init__(self):
        self.prompts_file = os.path.join(os.path.dirname(__file__), "..", "config", "prompts.json")
        self.custom_prompts_file = os.path.join(CHROMA_DB_PATH, "custom_prompts.json")
        self.default_prompts = self._load_default_prompts()
        self.custom_prompts = self._load_custom_prompts()

    def _load_default_prompts(self) -> Dict:
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载默认提示词失败: {e}")
            return {}

    def _load_custom_prompts(self) -> Dict:
        try:
            if os.path.exists(self.custom_prompts_file):
                with open(self.custom_prompts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载自定义提示词失败: {e}")
        return {}

    def _save_custom_prompts(self):
        try:
            os.makedirs(os.path.dirname(self.custom_prompts_file), exist_ok=True)
            with open(self.custom_prompts_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_prompts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存自定义提示词失败: {e}")

    def get_prompt(self, prompt_id: str) -> Optional[Dict]:
        if prompt_id in self.custom_prompts:
            return self.custom_prompts[prompt_id]
        if prompt_id in self.default_prompts:
            return self.default_prompts[prompt_id]
        return None

    def save_custom_prompt(self, prompt_id: str, name: str, content: str,
                           category: str = "custom", temperature: float = 0.7,
                           max_tokens: int = 2048) -> bool:
        try:
            self.custom_prompts[prompt_id] = {
                "name": name,
                "category": category,
                "system_prompt": content,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            self._save_custom_prompts()
            return True
        except Exception as e:
            print(f"保存自定义提示词失败: {e}")
            return False

    def delete_custom_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self.custom_prompts:
            del self.custom_prompts[prompt_id]
            self._save_custom_prompts()
            return True
        return False

    def list_prompts(self, category: Optional[str] = None) -> List[Dict]:
        all_prompts = []
        for pid, prompt in self.default_prompts.items():
            if category is None or prompt.get("category") == category:
                all_prompts.append({"id": pid, **prompt, "is_custom": False})
        for pid, prompt in self.custom_prompts.items():
            if category is None or prompt.get("category") == category:
                all_prompts.append({"id": pid, **prompt, "is_custom": True})
        return all_prompts

    def get_categories(self) -> List[str]:
        categories = set()
        for prompt in self.default_prompts.values():
            categories.add(prompt.get("category", "uncategorized"))
        for prompt in self.custom_prompts.values():
            categories.add(prompt.get("category", "uncategorized"))
        return sorted(list(categories))

    def update_custom_prompt(self, prompt_id: str, **kwargs) -> bool:
        if prompt_id not in self.custom_prompts:
            return False
        prompt = self.custom_prompts[prompt_id]
        for key, value in kwargs.items():
            if key in prompt:
                prompt[key] = value
        self._save_custom_prompts()
        return True

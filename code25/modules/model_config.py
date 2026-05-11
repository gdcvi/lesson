"""模型配置管理模块 —— 扩展多模态模型选项"""
import os
import json
from typing import Dict, Optional


class ModelConfigManager:
    """模型配置管理类"""

    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "data", "model_config.json")
        self.default_config = {
            "llm_model": "qwen-plus",
            "vision_model": "qwen-vl-plus",
            "embedding_model": "text-embedding-v3",
            "t2i_model": "wan2.2-t2i-flash",
            "i2v_model": "wanx2.1-i2v-turbo",
            "tts_model": "cosyvoice-v2",
            "tts_voice": "longxiaochun_v2",
            "asr_model": "paraformer-v2",
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_k": 5,
            "chunk_size": 1000,
            "chunk_overlap": 200,
        }
        self.current_config = self._load_config()

    def _load_config(self) -> Dict:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    config = self.default_config.copy()
                    config.update(saved_config)
                    return config
        except Exception as e:
            print(f"加载配置失败: {e}")
        return self.default_config.copy()

    def _save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def get_config(self) -> Dict:
        return self.current_config.copy()

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.current_config:
                self.current_config[key] = value
        self._save_config()

    def reset_to_default(self):
        self.current_config = self.default_config.copy()
        self._save_config()

    def create_preset(self, name: str, config: Dict) -> bool:
        try:
            presets_file = os.path.join(os.path.dirname(__file__), "..", "data", "presets.json")
            presets = {}
            if os.path.exists(presets_file):
                with open(presets_file, 'r', encoding='utf-8') as f:
                    presets = json.load(f)
            presets[name] = config
            with open(presets_file, 'w', encoding='utf-8') as f:
                json.dump(presets, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"创建预设失败: {e}")
            return False

    def load_preset(self, name: str) -> bool:
        try:
            presets_file = os.path.join(os.path.dirname(__file__), "..", "data", "presets.json")
            if not os.path.exists(presets_file):
                return False
            with open(presets_file, 'r', encoding='utf-8') as f:
                presets = json.load(f)
            if name in presets:
                self.current_config = presets[name]
                self._save_config()
                return True
            return False
        except Exception as e:
            print(f"加载预设失败: {e}")
            return False

    def list_presets(self) -> list:
        try:
            presets_file = os.path.join(os.path.dirname(__file__), "..", "data", "presets.json")
            if not os.path.exists(presets_file):
                return []
            with open(presets_file, 'r', encoding='utf-8') as f:
                presets = json.load(f)
            return list(presets.keys())
        except Exception as e:
            print(f"列出预设失败: {e}")
            return []

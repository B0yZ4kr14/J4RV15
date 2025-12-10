import yaml
import json
import configparser
import os
from pathlib import Path

class ConfigurationAgent:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def run_task(self, task: dict):
        action = task.get("action")
        params = task.get("params", {})
        
        if action == "get_config":
            return self._get_config(params.get("file_path"), params.get("key"))
        elif action == "set_config":
            return self._set_config(params.get("file_path"), params.get("key"), params.get("value"))
        else:
            return {"status": "ERROR", "message": f"Ação desconhecida: {action}"}

    def _get_file_handler(self, file_path: Path):
        ext = file_path.suffix.lower()
        if ext == ".yaml" or ext == ".yml":
            return self._handle_yaml
        elif ext == ".json":
            return self._handle_json
        elif ext == ".ini":
            return self._handle_ini
        else:
            return None

    def _get_config(self, file_path: str, key: str):
        full_path = self.base_path / file_path
        handler = self._get_file_handler(full_path)
        if not handler:
            return {"status": "ERROR", "message": f"Formato de arquivo não suportado: {full_path.suffix}"}
        
        try:
            config = handler("read", full_path)
            value = config.get(key, None)
            return {"status": "SUCCESS", "key": key, "value": value}
        except FileNotFoundError:
            return {"status": "ERROR", "message": f"Arquivo não encontrado: {full_path}"}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def _set_config(self, file_path: str, key: str, value):
        full_path = self.base_path / file_path
        handler = self._get_file_handler(full_path)
        if not handler:
            return {"status": "ERROR", "message": f"Formato de arquivo não suportado: {full_path.suffix}"}

        try:
            config = handler("read", full_path) if full_path.exists() else {}
            old_value = config.get(key)
            config[key] = value
            handler("write", full_path, config)
            return {"status": "SUCCESS", "key": key, "old_value": old_value, "new_value": value}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def _handle_yaml(self, mode: str, path: Path, data=None):
        if mode == "read":
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        elif mode == "write":
            with open(path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)

    def _handle_json(self, mode: str, path: Path, data=None):
        if mode == "read":
            with open(path, 'r') as f:
                return json.load(f)
        elif mode == "write":
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

    def _handle_ini(self, mode: str, path: Path, data=None):
        parser = configparser.ConfigParser()
        if mode == "read":
            parser.read(path)
            # Convert to dict for consistency
            config_dict = {s: dict(parser.items(s)) for s in parser.sections()}
            return config_dict
        elif mode == "write":
            # Assumes data is a dict of dicts
            for section, values in data.items():
                parser[section] = values
            with open(path, 'w') as f:
                parser.write(f)

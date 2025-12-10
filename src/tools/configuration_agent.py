import yaml
import json
import configparser
import os

class ConfigurationAgent:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        old_value = self.config.get(key)
        self.config[key] = value
        self._save_config()
        return {
            "status": "SUCCESS",
            "key": key,
            "old_value": old_value,
            "new_value": value
        }

    def j4_config(self, args):
        if len(args) == 2 and args[0] == 'get':
            return self.get(args[1])
        elif len(args) == 3 and args[0] == 'set':
            return self.set(args[1], args[2])
        else:
            return {"status": "ERROR", "message": "Invalid arguments"}

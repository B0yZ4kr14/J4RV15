'''
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import yaml
import psycopg2
from pathlib import Path
from typing import Dict, List, Any

class LLMManagerAgent:
    def __init__(self, db_params: Dict[str, str], system_context: Dict[str, Any]):
        """
        Inicializa o LLMManagerAgent.

        :param db_params: Dicionário com parâmetros de conexão ao banco de dados (dbname, user, password, host, port).
        :param system_context: Dicionário com o contexto do sistema detectado pelo SystemDetectorAgent.
        """
        self.db_params = db_params
        self.system_context = system_context
        self.config_path = Path.home() / ".J.4.R.V.1.5" / "10_configs" / "litellm" / "config.yaml"
        self.results = {}
        self._ensure_directories()
        self._init_db()

    def _ensure_directories(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def _run_command(self, command: str) -> (bool, str):
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, f"Command failed: {e.stderr}"

    def _db_execute(self, query: str, params: tuple = None, fetch=False):
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()
            cur.execute(query, params or ())
            if fetch:
                return cur.fetchall()
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Database Error: {error}")
            return None
        finally:
            if conn is not None:
                conn.close()

    def _init_db(self):
        """Cria a tabela de modelos se ela não existir."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS llm_models (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(255) UNIQUE NOT NULL,
            family VARCHAR(100),
            size_gb INT,
            type VARCHAR(20), -- 'local' or 'remote'
            is_pulled BOOLEAN DEFAULT FALSE,
            last_pulled_at TIMESTAMP
        );
        """
        self._db_execute(create_table_query)

    def _get_hardware_tier(self) -> str:
        """Determina o tier de hardware (CPU, GPU_SMALL, GPU_LARGE) com base no contexto do sistema."""
        if "gpu" in self.system_context.get("hardware", {}) and self.system_context["hardware"]["gpu"].get("vram_gb", 0) > 0:
            vram = self.system_context["hardware"]["gpu"]["vram_gb"]
            if vram >= 16:
                return "GPU_LARGE"
            else:
                return "GPU_SMALL"
        return "CPU"

    def _get_models_for_tier(self, tier: str) -> List[Dict[str, Any]]:
        """Retorna uma lista de modelos recomendados para um determinado tier de hardware."""
        model_map = {
            "CPU": [
                {"name": "llama3.1:8b-instruct-q4_K_M", "family": "llama", "size": 5, "type": "local"},
                {"name": "mistral:7b-instruct-v0.3-q4_K_M", "family": "mistral", "size": 4.3, "type": "local"}
            ],
            "GPU_SMALL": [
                {"name": "llama3.1:8b-instruct-fp16", "family": "llama", "size": 16, "type": "local"},
                {"name": "codellama:13b", "family": "codellama", "size": 7.4, "type": "local"}
            ],
            "GPU_LARGE": [
                {"name": "llama3.1:70b-instruct-q4_K_M", "family": "llama", "size": 42, "type": "local"},
                {"name": "codellama:34b", "family": "codellama", "size": 19, "type": "local"}
            ]
        }
        return model_map.get(tier, [])

    def pull_local_models(self) -> Dict:
        """Baixa os modelos locais do Ollama com base no tier de hardware."""
        tier = self._get_hardware_tier()
        models_to_pull = self._get_models_for_tier(tier)
        pull_results = {"status": "SUCCESS", "pulled_models": [], "errors": []}

        for model in models_to_pull:
            print(f"Puxando modelo para o tier {tier}: {model['name']}...")
            success, output = self._run_command(f"ollama pull {model['name']}")
            if success:
                pull_results["pulled_models"].append(model['name'])
                # Atualiza o banco de dados
                self._db_execute(
                    "INSERT INTO llm_models (model_name, family, size_gb, type, is_pulled, last_pulled_at) VALUES (%s, %s, %s, %s, TRUE, NOW()) ON CONFLICT (model_name) DO UPDATE SET is_pulled = TRUE, last_pulled_at = NOW();",
                    (model['name'], model['family'], model['size'], model['type'])
                )
            else:
                pull_results["errors"].append({model['name']: output})
                pull_results["status"] = "PARTIAL"
        
        return pull_results

    def generate_litellm_config(self, enabled_apis: List[str]) -> Dict:
        """Gera o arquivo de configuração do LiteLLM com base nos modelos locais e APIs remotas."""
        config_results = {"status": "SUCCESS", "config_path": str(self.config_path), "errors": []}
        
        model_list = []

        # Adiciona modelos locais (puxados com sucesso)
        local_models = self._db_execute("SELECT model_name FROM llm_models WHERE is_pulled = TRUE AND type = 'local';", fetch=True)
        if local_models:
            for (model_name,) in local_models:
                model_list.append({
                    "model_name": f"ollama/{model_name}",
                    "litellm_params": {
                        "model": f"ollama/{model_name}",
                        "api_base": "http://localhost:11434"
                    }
                })

        # Adiciona modelos de API remotos
        api_map = {
            "openai": {"model_name": "gpt-4o", "litellm_params": {"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}},
            "anthropic": {"model_name": "claude-3-5-sonnet", "litellm_params": {"model": "claude-3-5-sonnet-20240620", "api_key": os.environ.get("ANTHROPIC_API_KEY")}},
            "groq": {"model_name": "groq/llama3-70b-8192", "litellm_params": {"model": "groq/llama3-70b-8192", "api_key": os.environ.get("GROQ_API_KEY")}}
        }

        for api in enabled_apis:
            if api in api_map:
                model_list.append(api_map[api])

        # Configuração do roteador
        router_settings = {
            "enable_fallback": True,
            "set_verbose": True
        }

        final_config = {
            "model_list": model_list,
            "router_settings": router_settings
        }

        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(final_config, f, indent=2)
        except Exception as e:
            config_results["status"] = "FAILED"
            config_results["errors"].append(f"Falha ao escrever o arquivo de configuração: {e}")

        return config_results

    def execute(self, task: Dict) -> Dict:
        action = task.get("action")
        results = {}

        if action == "configure_llms":
            results["pull_status"] = self.pull_local_models()
            results["config_status"] = self.generate_litellm_config(task.get("enabled_apis", []))
        else:
            return {"status": "UNKNOWN_ACTION", "error": f"Ação desconhecida: {action}"}
        
        return results

if __name__ == '__main__':
    # Exemplo de uso
    # 1. Obter o contexto do sistema (simulado aqui)
    mock_system_context = {
        "hardware": {
            "gpu": {"vram_gb": 24}
        }
    }
    # 2. Parâmetros do DB (usar variáveis de ambiente na produção)
    mock_db_params = {
        "dbname": "j4rv15_db",
        "user": "j4rv15_user",
        "password": "secure_password",
        "host": "localhost",
        "port": "5432"
    }

    agent = LLMManagerAgent(db_params=mock_db_params, system_context=mock_system_context)

    task_prompt = {
        "action": "configure_llms",
        "enabled_apis": ["openai", "groq"]
    }

    final_results = agent.execute(task_prompt)
    print(json.dumps(final_results, indent=2))
'''

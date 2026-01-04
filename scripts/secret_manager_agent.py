#!/usr/bin/env python3
"""
SecretManagerAgent - Agente Gestor de Secrets .J.4.R.V.1.5.
Versão: 5.0.0
Autor: B0.y_Z4kr14

Responsabilidades:
- Auditar a estrutura de diretórios de segredos
- Normalizar permissões
- Detectar inconsistências
- Orquestrar migração para pass
- Gerar relatórios de auditoria
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List

# Import shared utilities
from j4rv15_common import (
    get_secrets_path,
    normalize_permissions,
    check_incorrect_permissions,
    SECURE_DIR_PERMS,
    SECURE_FILE_PERMS
)

class SecretManagerAgent:
    def __init__(self, secrets_base_path: str = None):
        """Inicializa o agente com o caminho base para os segredos."""
        if secrets_base_path is None:
            self.secrets_path = get_secrets_path()
        else:
            self.secrets_path = Path(secrets_base_path)
        
        self.expected_structure = {
            ".certificates": "Certificados SSL/TLS",
            ".env": "Arquivo de ambiente principal (legado)",
            ".env.d": "Diretório para múltiplos arquivos .env (legado)",
            ".gpg": "Chaves GPG (link simbólico para ~/.gnupg)",
            ".keys": "Chaves de API e outros tokens brutos (legado)",
            ".passwords": "Senhas em texto plano (legado)",
            ".tokens": "Tokens de autenticação (legado)",
            ".ssh": "Chaves SSH (link simbólico para ~/.ssh)"
        }

    def run_task(self, task: Dict):
        """Ponto de entrada principal para todas as tarefas do agente."""
        action = task.get("action")
        
        if action == "audit":
            return self._audit_secrets_structure()
        elif action == "normalize_permissions":
            return self._normalize_permissions()
        elif action == "detect_inconsistencies":
            return self._detect_inconsistencies()
        elif action == "prepare_migration":
            return self._prepare_migration()
        else:
            return {"status": "ERROR", "message": f"Ação desconhecida: {action}"}

    def _audit_secrets_structure(self):
        """Audita a estrutura de diretórios de segredos."""
        if not self.secrets_path.exists():
            return {
                "status": "ERROR",
                "message": f"Diretório de segredos não encontrado: {self.secrets_path}"
            }
        
        audit_results = {
            "status": "OK",
            "secrets_path": str(self.secrets_path),
            "structure": {},
            "missing_components": []
        }
        
        for component, description in self.expected_structure.items():
            component_path = self.secrets_path / component
            if component_path.exists():
                audit_results["structure"][component] = {
                    "exists": True,
                    "type": "symlink" if component_path.is_symlink() else ("directory" if component_path.is_dir() else "file"),
                    "description": description
                }
            else:
                audit_results["missing_components"].append(component)
        
        return audit_results

    def _normalize_permissions(self):
        """Normaliza as permissões de arquivos e diretórios."""
        if not self.secrets_path.exists():
            return {
                "status": "ERROR",
                "message": f"Diretório de segredos não encontrado: {self.secrets_path}"
            }
        
        # Use the shared utility function
        normalized_items = normalize_permissions(
            self.secrets_path,
            dir_perms=SECURE_DIR_PERMS,
            file_perms=SECURE_FILE_PERMS
        )
        
        return {
            "status": "OK",
            "message": f"Permissões normalizadas para {len(normalized_items)} itens",
            "normalized_items": normalized_items
        }

    def _detect_inconsistencies(self):
        """Detecta inconsistências na estrutura de segredos."""
        if not self.secrets_path.exists():
            return {
                "status": "ERROR",
                "message": f"Diretório de segredos não encontrado: {self.secrets_path}"
            }
        
        # Use the shared utility function
        incorrect_dirs, incorrect_files = check_incorrect_permissions(
            self.secrets_path,
            expected_dir_perms=SECURE_DIR_PERMS,
            expected_file_perms=SECURE_FILE_PERMS
        )
        
        inconsistencies = {
            "incorrect_permissions": incorrect_dirs + incorrect_files,
            "orphan_files": [],
            "unexpected_items": []
        }
        
        return {
            "status": "OK",
            "inconsistencies": inconsistencies
        }

    def _prepare_migration(self):
        """Prepara o ambiente para migração para pass."""
        # Verifica se o pass está instalado
        try:
            subprocess.run(["which", "pass"], check=True, capture_output=True)
            pass_installed = True
        except subprocess.CalledProcessError:
            pass_installed = False
        
        # Verifica se o pass está inicializado
        pass_store = Path.home() / ".password-store"
        pass_initialized = pass_store.exists()
        
        # Conta os segredos a serem migrados
        legacy_secrets_count = 0
        legacy_paths = [".passwords", ".tokens", ".keys"]
        
        for legacy_path in legacy_paths:
            path = self.secrets_path / legacy_path
            if path.exists() and path.is_dir():
                legacy_secrets_count += len(list(path.iterdir()))
        
        return {
            "status": "OK",
            "pass_installed": pass_installed,
            "pass_initialized": pass_initialized,
            "legacy_secrets_count": legacy_secrets_count,
            "ready_for_migration": pass_installed and pass_initialized
        }

if __name__ == "__main__":
    agent = SecretManagerAgent()
    
    # Exemplo de uso
    task = {"action": "audit"}
    result = agent.run_task(task)
    print(json.dumps(result, indent=2))

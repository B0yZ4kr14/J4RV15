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

import os
import stat
import subprocess
import json
from pathlib import Path
from typing import Dict, List

class SecretManagerAgent:
    def __init__(self, secrets_base_path: str = None):
        """Inicializa o agente com o caminho base para os segredos."""
        if secrets_base_path is None:
            home = Path.home()
            self.secrets_path = home / ".J.4.R.V.1.5" / "60_secrets"
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
        """Normaliza as permissões de arquivos e diretórios de forma eficiente."""
        if not self.secrets_path.exists():
            return {
                "status": "ERROR",
                "message": f"Diretório de segredos não encontrado: {self.secrets_path}"
            }
        
        normalized_items = []
        
        # Uma única passagem por toda a árvore de diretórios
        for root, dirs, files in os.walk(self.secrets_path):
            root_path = Path(root)
            
            # Normaliza permissões de diretórios para 700
            for dir_name in dirs:
                dir_path = root_path / dir_name
                if not dir_path.is_symlink():
                    current_perms = stat.S_IMODE(dir_path.stat().st_mode)
                    if current_perms != 0o700:
                        dir_path.chmod(0o700)
                        normalized_items.append(str(dir_path))
            
            # Normaliza permissões de arquivos para 600
            for file_name in files:
                file_path = root_path / file_name
                if not file_path.is_symlink():
                    current_perms = stat.S_IMODE(file_path.stat().st_mode)
                    if current_perms != 0o600:
                        file_path.chmod(0o600)
                        normalized_items.append(str(file_path))
        
        return {
            "status": "OK",
            "message": f"Permissões normalizadas para {len(normalized_items)} itens",
            "normalized_items": normalized_items
        }

    def _detect_inconsistencies(self):
        """Detecta inconsistências na estrutura de segredos de forma eficiente."""
        if not self.secrets_path.exists():
            return {
                "status": "ERROR",
                "message": f"Diretório de segredos não encontrado: {self.secrets_path}"
            }
        
        inconsistencies = {
            "incorrect_permissions": [],
            "orphan_files": [],
            "unexpected_items": []
        }
        
        # Uma única passagem por toda a árvore
        for root, dirs, files in os.walk(self.secrets_path):
            root_path = Path(root)
            
            # Verificar permissões de arquivos
            for file_name in files:
                file_path = root_path / file_name
                if not file_path.is_symlink():
                    current_perms = stat.S_IMODE(file_path.stat().st_mode)
                    if current_perms != 0o600:
                        inconsistencies["incorrect_permissions"].append(str(file_path))
        
        return {
            "status": "OK",
            "inconsistencies": inconsistencies
        }

    def _prepare_migration(self):
        """Prepara o ambiente para migração para pass (versão otimizada)."""
        # Cache dos resultados de subprocess para evitar chamadas repetidas
        pass_installed = False
        try:
            # Usar shutil.which é mais eficiente que subprocess
            import shutil
            pass_installed = shutil.which("pass") is not None
        except Exception:
            pass
        
        # Verificar se o pass está inicializado
        pass_store = Path.home() / ".password-store"
        pass_initialized = pass_store.exists()
        
        # Contar os segredos a serem migrados de forma eficiente
        legacy_secrets_count = 0
        legacy_paths = [".passwords", ".tokens", ".keys"]
        
        for legacy_path in legacy_paths:
            path = self.secrets_path / legacy_path
            if path.exists() and path.is_dir():
                # Usar scandir() é mais eficiente que iterdir()
                try:
                    with os.scandir(path) as entries:
                        legacy_secrets_count += sum(1 for entry in entries if entry.is_file())
                except OSError:
                    pass
        
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

#!/usr/bin/env python3
"""
J4RV15 v1.0 - Core Structure
Implementação conforme especificação v2.1.1
Com todas as correções de segurança da análise Popperiana
"""

import os
import sys
import json
import hashlib
import tempfile
import fcntl
import subprocess
import shutil
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from contextlib import contextmanager

# Configuração de segurança
UMASK_SECURE = 0o077
os.umask(UMASK_SECURE)

# Custom exception for security errors
class SecurityError(Exception):
    """Raised when a security violation is detected"""
    pass

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
)
logger = logging.getLogger('J4RV15.v7')

# =====================================================
# ESTRUTURA CANÔNICA EXATA DO DOCUMENTO v2.1.1
# =====================================================

J4RV15_ROOT = Path.home() / ".J.4.R.V.1.5"  # Exatamente assim!

CANONICAL_STRUCTURE = {
    "00_.local": {
        "purpose": "XDG-Style Local Data",
        "permissions": 0o755,
        "subdirs": ["bin", "lib", "share", "state", "cache", "config"]
    },
    "00_logs": {
        "purpose": "Logs e Auditoria",
        "permissions": 0o755,
        "subdirs": ["audit", "cleanup", "backup", "tree", "forensic"]
    },
    "01_saas_foundry": {
        "purpose": "Projetos e Tools",
        "permissions": 0o755,
        "subdirs": [
            "tools",  # Scripts J4RV15 aqui
            "src",
            "docs",
            "containers/vms",
            "containers/docker",
            "containers/k8s"
        ]
    },
    "10_configs": {
        "purpose": "Configurações de Apps",
        "permissions": 0o755,
        "subdirs": [
            "apps",
            "editors", 
            "git",
            "ides/vscode",
            "ides/cursor",
            "ides/neovim",
            "mcp",
            "shell",
            "terminal",
            "wm"
        ]
    },
    "20_workspace": {
        "purpose": "Trabalho Ativo",
        "permissions": 0o755,
        "subdirs": ["current", "scratch"]
    },
    "30_knowledge": {
        "purpose": "Documentação",
        "permissions": 0o755,
        "subdirs": ["docs", "notes", "references"]
    },
    "40_infrastructure": {
        "purpose": "IaC (sem VMs!)",
        "permissions": 0o755,
        "subdirs": ["ansible", "terraform", "k8s", "scripts"]
    },
    "50_templates": {
        "purpose": "Templates",
        "permissions": 0o755,
        "subdirs": ["code", "configs", "docs"]
    },
    "60_secrets": {
        "purpose": "Secrets (SECURE)",
        "permissions": 0o700,  # Mais restritivo!
        "subdirs": [
            ".ssh",      # SSH keys (oculto)
            ".gpg",      # GPG keys (oculto)
            ".env.d",    # Envs modulares (oculto)
            ".tokens",   # API tokens (oculto)
            ".certs",    # Certificados (oculto)
            ".keys",     # Chaves genéricas (oculto)
            ".2fa",      # 2FA codes (oculto)
            ".vault"     # Vault secrets (oculto)
        ],
        "files": [
            ".env"       # Env unificado
        ]
    },
    "70_media": {
        "purpose": "Mídia",
        "permissions": 0o755,
        "subdirs": ["images", "videos", "audio", "screenshots"]
    },
    "80_bin": {
        "purpose": "Executáveis (PATH)",
        "permissions": 0o755,
        "subdirs": []
    },
    "90_tmp": {
        "purpose": "Temporário",
        "permissions": 0o755,
        "subdirs": ["downloads", "build", "cache"]
    },
    "99_archive": {
        "purpose": "Arquivamento",
        "permissions": 0o755,
        "subdirs": ["old", "backup", "legacy"]
    }
}

# Diretórios que devem ser migrados se encontrados no root
LEGACY_DIRS_TO_MIGRATE = {
    "vms": "01_saas_foundry/containers/vms",
    "vscode": "10_configs/ides/vscode",
    "00_secrets": "60_secrets"  # Renomear para o padrão correto
}


@contextmanager
def secure_umask(umask_value: int = UMASK_SECURE):
    """Context manager para umask temporário seguro"""
    old = os.umask(umask_value)
    try:
        yield
    finally:
        os.umask(old)


@contextmanager
def file_lock(path: Path, exclusive: bool = True):
    """File lock para prevenir race conditions (TOCTOU fix)"""
    lock_file = Path(f"{path}.lock")
    fd = os.open(str(lock_file), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        fcntl.flock(fd, lock_type)
        yield fd
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        try:
            lock_file.unlink()
        except:
            pass


class SecureFileOps:
    """Operações de arquivo seguras com prevenção de TOCTOU e path traversal"""
    
    @staticmethod
    def validate_path(base_path: Path, target_path: Path) -> Path:
        """Valida path para prevenir path traversal"""
        base = base_path.resolve()
        target = target_path.resolve()
        
        try:
            target.relative_to(base)
        except ValueError:
            raise SecurityError(f"Path traversal detectado: {target} não está em {base}")
        
        # Verificar symlinks no caminho
        current = base
        for part in target.relative_to(base).parts:
            current = current / part
            if current.is_symlink():
                raise SecurityError(f"Symlink detectado: {current}")
        
        return target
    
    @staticmethod
    def atomic_write(path: Path, content: bytes, mode: int = 0o644) -> None:
        """Escrita atômica de arquivo"""
        path = Path(path)
        dir_path = path.parent
        dir_path.mkdir(parents=True, exist_ok=True, mode=0o755)
        
        # Criar arquivo temporário no mesmo diretório
        with tempfile.NamedTemporaryFile(
            dir=dir_path,
            delete=False,
            mode='wb',
            prefix=f".{path.name}.",
            suffix='.tmp'
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)
            
            try:
                # Escrever conteúdo
                tmp_file.write(content)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
                
                # Definir permissões antes do rename
                os.fchmod(tmp_file.fileno(), mode)
                
                # Rename atômico
                tmp_path.rename(path)
                
                # Sync do diretório
                dir_fd = os.open(str(dir_path), os.O_RDONLY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
                    
            except Exception:
                try:
                    tmp_path.unlink()
                except:
                    pass
                raise


class J4RV15BrutalistSystem:
    """Sistema J4RV15 seguindo exatamente a especificação Core v2.1.1"""
    
    def __init__(self):
        self.root = J4RV15_ROOT
        self.file_ops = SecureFileOps()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.created_dirs: List[Path] = []
        self.migrated_items: List[Tuple[Path, Path]] = []
        
    def initialize_structure(self) -> bool:
        """Cria a estrutura canônica completa (versão otimizada)"""
        logger.info(f"Inicializando estrutura J4RV15 em {self.root}")
        
        try:
            # Criar root se não existir
            self.root.mkdir(parents=True, exist_ok=True, mode=0o755)
            
            # Criar cada diretório canônico
            for dir_name, config in CANONICAL_STRUCTURE.items():
                dir_path = self.root / dir_name
                dir_exists = dir_path.exists()  # Cache do resultado exists()
                
                # Criar diretório principal
                if not dir_exists:
                    with secure_umask():
                        dir_path.mkdir(mode=config["permissions"], exist_ok=True)
                        self.created_dirs.append(dir_path)
                        logger.info(f"Criado: {dir_name} ({oct(config['permissions'])})")
                    dir_exists = True  # Atualizar cache
                
                # Aplicar permissões corretas mesmo se já existir
                if dir_exists:
                    current_mode = dir_path.stat().st_mode & 0o777
                    if current_mode != config["permissions"]:
                        dir_path.chmod(config["permissions"])
                        logger.info(f"Permissões corrigidas: {dir_name} -> {oct(config['permissions'])}")
                
                # Criar subdiretórios
                for subdir in config.get("subdirs", []):
                    # Suporta paths aninhados como "containers/vms"
                    subdir_path = dir_path / subdir
                    if not subdir_path.exists():
                        # Para diretórios em 60_secrets, usar permissões mais restritivas
                        if dir_name == "60_secrets":
                            subdir_path.mkdir(parents=True, exist_ok=True, mode=0o700)
                        else:
                            subdir_path.mkdir(parents=True, exist_ok=True, mode=0o755)
                        logger.info(f"  Subdir criado: {subdir}")
                
                # Criar arquivos especiais (como .env)
                for file_name in config.get("files", []):
                    file_path = dir_path / file_name
                    if not file_path.exists():
                        file_path.touch(mode=0o600)
                        logger.info(f"  Arquivo criado: {file_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na inicialização: {e}")
            self.errors.append(str(e))
            return False
    
    def migrate_legacy_items(self) -> None:
        """Migra diretórios legados para locais corretos"""
        logger.info("Verificando itens legados para migração")
        
        for old_name, new_location in LEGACY_DIRS_TO_MIGRATE.items():
            old_path = self.root / old_name
            new_path = self.root / new_location
            
            if old_path.exists() and old_path.is_dir():
                logger.info(f"Migrando: {old_name} -> {new_location}")
                
                try:
                    # Criar diretório de destino se necessário
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Se o destino já existe, fazer merge
                    if new_path.exists():
                        # Copiar conteúdo item por item
                        for item in old_path.iterdir():
                            dest_item = new_path / item.name
                            if not dest_item.exists():
                                shutil.move(str(item), str(dest_item))
                                logger.info(f"  Movido: {item.name}")
                        # Remover diretório vazio
                        if not list(old_path.iterdir()):
                            old_path.rmdir()
                    else:
                        # Mover diretório inteiro
                        shutil.move(str(old_path), str(new_path))
                    
                    self.migrated_items.append((old_path, new_path))
                    logger.info(f"  Migração concluída: {old_name}")
                    
                except Exception as e:
                    logger.error(f"Erro migrando {old_name}: {e}")
                    self.errors.append(f"Migration failed: {old_name}: {e}")
    
    def fix_permissions(self) -> None:
        """Corrige permissões de segurança de forma eficiente"""
        logger.info("Aplicando permissões de segurança")
        
        # 60_secrets precisa de tratamento especial
        secrets_dir = self.root / "60_secrets"
        if not secrets_dir.exists():
            return
            
        # Diretório principal: 700
        secrets_dir.chmod(0o700)
        
        # Usar os.walk() uma única vez para percorrer toda a árvore
        # Isso é muito mais eficiente do que iterdir() aninhados
        for root, dirs, files in os.walk(secrets_dir):
            root_path = Path(root)
            
            # Aplicar permissões aos diretórios
            for dir_name in dirs:
                dir_path = root_path / dir_name
                if not dir_path.is_symlink():
                    dir_path.chmod(0o700)
            
            # Aplicar permissões aos arquivos
            for file_name in files:
                file_path = root_path / file_name
                if not file_path.is_symlink():
                    file_path.chmod(0o600)
        
        logger.info("Permissões de 60_secrets aplicadas (700/600)")
    
    def create_tools_scripts(self) -> None:
        """Cria os scripts principais em 01_saas_foundry/tools/"""
        tools_dir = self.root / "01_saas_foundry" / "tools"
        tools_dir.mkdir(parents=True, exist_ok=True)
        
        # j4rv15_core.py - Módulo base
        core_content = '''#!/usr/bin/env python3
"""J4RV15 Core - Constantes e configurações base"""

from pathlib import Path

# Raiz do J4RV15 - EXATAMENTE como especificado
J4RV15_ROOT = Path.home() / ".J.4.R.V.1.5"

# Versão
VERSION = "7.0.0"

# Estrutura canônica
CANONICAL_DIRS = [
    "00_.local",
    "00_logs",
    "01_saas_foundry",
    "10_configs",
    "20_workspace",
    "30_knowledge",
    "40_infrastructure",
    "50_templates",
    "60_secrets",
    "70_media",
    "80_bin",
    "90_tmp",
    "99_archive"
]

# Diretórios que precisam permissões especiais
SECURE_DIRS = {
    "60_secrets": 0o700,
    "60_secrets/.ssh": 0o700,
    "60_secrets/.gpg": 0o700,
    "60_secrets/.env.d": 0o700,
}

print(f"J4RV15 Core v{VERSION} - Root: {J4RV15_ROOT}")
'''
        
        core_path = tools_dir / "j4rv15_core.py"
        self.file_ops.atomic_write(core_path, core_content.encode(), 0o755)
        
        # j4rv15_validate.py - Validação
        validate_content = '''#!/usr/bin/env python3
"""J4RV15 Validate - Validação da estrutura"""

from pathlib import Path
from j4rv15_core import J4RV15_ROOT, CANONICAL_DIRS

def validate_structure():
    """Valida se a estrutura está correta"""
    issues = []
    
    if not J4RV15_ROOT.exists():
        issues.append(f"Root não existe: {J4RV15_ROOT}")
        return issues
    
    for dir_name in CANONICAL_DIRS:
        dir_path = J4RV15_ROOT / dir_name
        if not dir_path.exists():
            issues.append(f"Diretório faltando: {dir_name}")
    
    # Verificar permissões de 60_secrets
    secrets_dir = J4RV15_ROOT / "60_secrets"
    if secrets_dir.exists():
        mode = secrets_dir.stat().st_mode & 0o777
        if mode != 0o700:
            issues.append(f"60_secrets com permissões incorretas: {oct(mode)}")
    
    return issues

if __name__ == "__main__":
    issues = validate_structure()
    if issues:
        print("❌ Problemas encontrados:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ Estrutura validada com sucesso!")
'''
        
        validate_path = tools_dir / "j4rv15_validate.py"
        self.file_ops.atomic_write(validate_path, validate_content.encode(), 0o755)
        
        logger.info(f"Scripts criados em {tools_dir}")
    
    def create_fish_functions(self) -> None:
        """Cria funções Fish para comandos j4*"""
        fish_content = '''# J4RV15 Fish Functions v1.0
# Comandos para navegação e gerenciamento

# Navegação principal
function j4
    cd ~/.J.4.R.V.1.5
end

function j4tools
    cd ~/.J.4.R.V.1.5/01_saas_foundry/tools
end

function j4secrets
    cd ~/.J.4.R.V.1.5/60_secrets
end

function j4logs
    cd ~/.J.4.R.V.1.5/00_logs
end

# Comandos de status
function j4status
    echo "🏗️ J4RV15 v1.0 - Core Structure"
    echo "Root: ~/.J.4.R.V.1.5"
    echo ""
    ls -la ~/.J.4.R.V.1.5/
end

function j4tree
    tree -L 2 ~/.J.4.R.V.1.5/
end

# Validação
function j4validate
    python3 ~/.J.4.R.V.1.5/01_saas_foundry/tools/j4rv15_validate.py
end

# Ajuda
function j4help
    echo "J4RV15 Commands:"
    echo "  j4         - Go to J4RV15 root"
    echo "  j4tools    - Go to tools directory"
    echo "  j4secrets  - Go to secrets directory"
    echo "  j4logs     - Go to logs directory"
    echo "  j4status   - Show status"
    echo "  j4tree     - Show directory tree"
    echo "  j4validate - Validate structure"
    echo "  j4help     - Show this help"
end
'''
        
        # Salvar em config/fish local
        fish_dir = Path.home() / ".config" / "fish" / "conf.d"
        fish_dir.mkdir(parents=True, exist_ok=True)
        
        fish_path = fish_dir / "j4rv15.fish"
        self.file_ops.atomic_write(fish_path, fish_content.encode(), 0o644)
        
        logger.info(f"Funções Fish criadas em {fish_path}")
    
    def create_install_script(self) -> None:
        """Cria script de instalação"""
        install_content = '''#!/bin/bash
# J4RV15 v1.0 Installation Script
# Core Structure

set -euo pipefail
IFS=$'\\n\\t'

echo "🏗️ J4RV15 v1.0 - Core Structure"
echo "Installation Script"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi

# Run Python installer
python3 - << 'EOF'
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from j4rv15_v7_brutalist import J4RV15BrutalistSystem

system = J4RV15BrutalistSystem()

print("1. Criando estrutura...")
if system.initialize_structure():
    print("   ✅ Estrutura criada")
else:
    print("   ❌ Erro criando estrutura")
    sys.exit(1)

print("2. Migrando itens legados...")
system.migrate_legacy_items()
print("   ✅ Migração concluída")

print("3. Aplicando permissões...")
system.fix_permissions()
print("   ✅ Permissões aplicadas")

print("4. Criando scripts...")
system.create_tools_scripts()
print("   ✅ Scripts criados")

print("5. Configurando Fish...")
system.create_fish_functions()
print("   ✅ Fish configurado")

print("")
print("✅ Instalação completa!")
print("")
print("Execute:")
print("  source ~/.config/fish/conf.d/j4rv15.fish")
print("  j4help")
EOF
'''
        
        install_path = self.root / "01_saas_foundry" / "tools" / "install.sh"
        install_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_ops.atomic_write(install_path, install_content.encode(), 0o755)
        
        logger.info(f"Script de instalação criado: {install_path}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório de operações"""
        return {
            "timestamp": datetime.now().isoformat(),
            "version": "7.0.0",
            "root": str(self.root),
            "created_dirs": [str(d) for d in self.created_dirs],
            "migrated_items": [(str(old), str(new)) for old, new in self.migrated_items],
            "errors": self.errors,
            "warnings": self.warnings,
            "status": "SUCCESS" if not self.errors else "COMPLETED_WITH_ERRORS"
        }


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='J4RV15 v1.0 - Core Structure'
    )
    
    parser.add_argument('--init', action='store_true',
                       help='Inicializar estrutura completa')
    parser.add_argument('--validate', action='store_true',
                       help='Validar estrutura existente')
    parser.add_argument('--migrate', action='store_true',
                       help='Migrar itens legados')
    parser.add_argument('--fix-permissions', action='store_true',
                       help='Corrigir permissões')
    parser.add_argument('--install-scripts', action='store_true',
                       help='Instalar scripts em tools/')
    
    args = parser.parse_args()
    
    system = J4RV15BrutalistSystem()
    
    if args.init:
        print("🏗️ J4RV15 v1.0 - Core Structure")
        print(f"Inicializando em {J4RV15_ROOT}")
        print("")
        
        if system.initialize_structure():
            system.migrate_legacy_items()
            system.fix_permissions()
            system.create_tools_scripts()
            system.create_fish_functions()
            system.create_install_script()
            
            print("")
            print("✅ Estrutura criada com sucesso!")
            print("")
            print("Estrutura canônica:")
            for dir_name in CANONICAL_STRUCTURE.keys():
                print(f"  📁 {dir_name}/")
            print("")
            print("Execute:")
            print("  source ~/.config/fish/conf.d/j4rv15.fish")
            print("  j4help")
        else:
            print("❌ Erro na inicialização")
            for error in system.errors:
                print(f"  • {error}")
    
    elif args.validate:
        # Validação simples
        issues = []
        
        if not J4RV15_ROOT.exists():
            issues.append("Root não existe")
        else:
            for dir_name in CANONICAL_STRUCTURE.keys():
                if not (J4RV15_ROOT / dir_name).exists():
                    issues.append(f"Faltando: {dir_name}")
        
        if issues:
            print("❌ Problemas encontrados:")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print("✅ Estrutura válida!")
    
    elif args.migrate:
        system.migrate_legacy_items()
        print("✅ Migração concluída")
    
    elif args.fix_permissions:
        system.fix_permissions()
        print("✅ Permissões corrigidas")
    
    elif args.install_scripts:
        system.create_tools_scripts()
        system.create_fish_functions()
        print("✅ Scripts instalados")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

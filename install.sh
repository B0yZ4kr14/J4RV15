#!/bin/bash
# J4RV15 v7.0.0 - Brutalist Purist Structure
# Instalador seguindo exatamente o documento v2.1.1

set -euo pipefail
IFS=$'\n\t'

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                              ║${NC}"
echo -e "${BLUE}║     ██╗██╗  ██╗██████╗ ██╗   ██╗ ██╗███████╗    ██╗   ██╗███████╗          ║${NC}"
echo -e "${BLUE}║     ██║██║  ██║██╔══██╗██║   ██║███║██╔════╝    ██║   ██║╚════██║          ║${NC}"
echo -e "${BLUE}║     ██║███████║██████╔╝██║   ██║╚██║███████╗    ██║   ██║    ██╔╝          ║${NC}"
echo -e "${BLUE}║██   ██║╚════██║██╔══██╗╚██╗ ██╔╝ ██║╚════██║    ╚██╗ ██╔╝   ██╔╝           ║${NC}"
echo -e "${BLUE}║╚█████╔╝     ██║██║  ██║ ╚████╔╝  ██║███████║     ╚████╔╝    ██║            ║${NC}"
echo -e "${BLUE}║ ╚════╝      ╚═╝╚═╝  ╚═╝  ╚═══╝   ╚═╝╚══════╝      ╚═══╝     ╚═╝            ║${NC}"
echo -e "${BLUE}║                                                                              ║${NC}"
echo -e "${BLUE}║                      Brutalist Purist Structure v7.0.0                      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificações de segurança
if [[ "${EUID}" -eq 0 ]]; then
    echo -e "${RED}❌ Erro: Não execute como root (risco de segurança)${NC}"
    exit 1
fi

# Definir umask seguro
umask 077

# Verificar Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado${NC}"
    exit 1
fi

# Verificar Fish
if ! command -v fish &>/dev/null; then
    echo -e "${YELLOW}⚠️ Fish shell não encontrado${NC}"
    echo "Instale com: sudo pacman -S fish"
fi

echo -e "${BLUE}[1/5] Instalando dependências Python...${NC}"
pip install --user --quiet rich psutil 2>/dev/null || true

echo -e "${BLUE}[2/5] Criando estrutura Brutalist Purist...${NC}"
python3 scripts/j4rv15_brutalist.py --init

echo -e "${BLUE}[3/5] Configurando Fish functions...${NC}"
if [ -d ~/.config/fish/conf.d ]; then
    cp fish/j4rv15.fish ~/.config/fish/conf.d/
    echo -e "  ${GREEN}✅ Fish configurado${NC}"
else
    echo -e "  ${YELLOW}⚠️ Fish não configurado (diretório não encontrado)${NC}"
fi

echo -e "${BLUE}[4/5] Instalando systemd service (opcional)...${NC}"
if [ -d ~/.config/systemd/user ]; then
    cp systemd/j4rv15.service ~/.config/systemd/user/
    echo -e "  ${GREEN}✅ Systemd service instalado${NC}"
else
    echo -e "  ${YELLOW}⚠️ Systemd não configurado${NC}"
fi

echo -e "${BLUE}[5/5] Validando instalação...${NC}"
python3 ~/.J.4.R.V.1.5/01_saas_foundry/tools/j4rv15_validate.py

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                         ✅ INSTALAÇÃO COMPLETA!                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Estrutura criada em: ~/.J.4.R.V.1.5/${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Carregue as funções Fish:"
echo "   source ~/.config/fish/conf.d/j4rv15.fish"
echo ""
echo "2. Teste os comandos:"
echo "   j4help      # Ver todos os comandos"
echo "   j4status    # Ver status"
echo "   j4tree      # Ver estrutura"
echo ""
echo -e "${GREEN}Filosofia Brutalist Purist:${NC}"
echo ""Explícito sobre implícito. Direto sobre abstrato. Transparente sobre mágico.""

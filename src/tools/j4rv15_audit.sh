#!/bin/sh
# Script de Auditoria do Sistema .J.4.R.V.1.5.
# Versão: 5.0.0
# Compatível com POSIX /bin/sh
# Modo: Somente leitura, não destrutivo

# Gera timestamp para o nome do arquivo de log
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$HOME/J4RV15_audit_${TIMESTAMP}.txt"

# Inicia o log
echo "========================================" > "$LOG_FILE"
echo "Auditoria do Sistema .J.4.R.V.1.5." >> "$LOG_FILE"
echo "Data: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 1. Informações de Hardware
echo "## 1. HARDWARE" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "CPU:" >> "$LOG_FILE"
lscpu | grep "Model name" >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
echo "GPU:" >> "$LOG_FILE"
lspci | grep -i vga >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
echo "RAM:" >> "$LOG_FILE"
free -h >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
echo "Discos:" >> "$LOG_FILE"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

# 2. Pacotes Instalados (Arch Linux)
echo "## 2. PACOTES INSTALADOS" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
pacman -Q | wc -l >> "$LOG_FILE" 2>&1
echo "pacotes instalados via pacman" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 3. Serviços Systemd
echo "## 3. SERVIÇOS SYSTEMD" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
systemctl list-units --type=service --state=running --no-pager >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

# 4. Estrutura de Segredos
echo "## 4. ESTRUTURA DE SEGREDOS" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
SECRETS_DIR="$HOME/.J.4.R.V.1.5/60_secrets"
if [ -d "$SECRETS_DIR" ]; then
    echo "Diretório de segredos encontrado: $SECRETS_DIR" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "Estrutura de diretórios:" >> "$LOG_FILE"
    tree -L 2 -d "$SECRETS_DIR" >> "$LOG_FILE" 2>&1 || ls -R "$SECRETS_DIR" >> "$LOG_FILE" 2>&1
    echo "" >> "$LOG_FILE"
else
    echo "AVISO: Diretório de segredos não encontrado em $SECRETS_DIR" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# 5. Permissões de Arquivos Sensíveis
echo "## 5. PERMISSÕES DE ARQUIVOS SENSÍVEIS" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
if [ -d "$SECRETS_DIR" ]; then
    find "$SECRETS_DIR" -type f -exec ls -lh {} \; | awk '{print $1, $9}' >> "$LOG_FILE" 2>&1
    echo "" >> "$LOG_FILE"
fi

# 6. Detecção de Inconsistências
echo "## 6. DETECÇÃO DE INCONSISTÊNCIAS" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
if [ -d "$SECRETS_DIR" ]; then
    echo "Verificando permissões incorretas (arquivos que não sejam 600 ou 700):" >> "$LOG_FILE"
    find "$SECRETS_DIR" -type f ! -perm 600 -exec ls -lh {} \; >> "$LOG_FILE" 2>&1
    find "$SECRETS_DIR" -type d ! -perm 700 -exec ls -lhd {} \; >> "$LOG_FILE" 2>&1
    echo "" >> "$LOG_FILE"
fi

# 7. Ambiente Gráfico
echo "## 7. AMBIENTE GRÁFICO" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
if [ -n "$WAYLAND_DISPLAY" ]; then
    echo "Ambiente: Wayland" >> "$LOG_FILE"
    echo "Display: $WAYLAND_DISPLAY" >> "$LOG_FILE"
elif [ -n "$DISPLAY" ]; then
    echo "Ambiente: X11" >> "$LOG_FILE"
    echo "Display: $DISPLAY" >> "$LOG_FILE"
else
    echo "Ambiente: TTY (sem ambiente gráfico)" >> "$LOG_FILE"
fi
echo "" >> "$LOG_FILE"

# 8. Integração com GPG
echo "## 8. INTEGRAÇÃO COM GPG" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
echo "Chaves GPG disponíveis:" >> "$LOG_FILE"
gpg --list-keys >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

# 9. Estrutura do pass
echo "## 9. ESTRUTURA DO PASS" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
if command -v pass > /dev/null 2>&1; then
    echo "pass está instalado" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "Estrutura do cofre:" >> "$LOG_FILE"
    pass ls >> "$LOG_FILE" 2>&1
    echo "" >> "$LOG_FILE"
else
    echo "AVISO: pass não está instalado" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# Finaliza o log
echo "========================================" >> "$LOG_FILE"
echo "Auditoria concluída" >> "$LOG_FILE"
echo "Log salvo em: $LOG_FILE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Exibe mensagem de conclusão
echo "Auditoria concluída. Log salvo em: $LOG_FILE"

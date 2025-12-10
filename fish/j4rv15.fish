# J4RV15 v7.0.0 - Fish Functions
# Brutalist Purist Structure - Comandos canônicos

# ============================================
# NAVEGAÇÃO PRINCIPAL
# ============================================

function j4
    cd ~/.J.4.R.V.1.5
end

function j4local
    cd ~/.J.4.R.V.1.5/00_.local
end

function j4logs
    cd ~/.J.4.R.V.1.5/00_logs
end

function j4saas
    cd ~/.J.4.R.V.1.5/01_saas_foundry
end

function j4tools
    cd ~/.J.4.R.V.1.5/01_saas_foundry/tools
end

function j4configs
    cd ~/.J.4.R.V.1.5/10_configs
end

function j4workspace
    cd ~/.J.4.R.V.1.5/20_workspace
end

function j4knowledge
    cd ~/.J.4.R.V.1.5/30_knowledge
end

function j4infra
    cd ~/.J.4.R.V.1.5/40_infrastructure
end

function j4templates
    cd ~/.J.4.R.V.1.5/50_templates
end

function j4secrets
    cd ~/.J.4.R.V.1.5/60_secrets
end

function j4media
    cd ~/.J.4.R.V.1.5/70_media
end

function j4bin
    cd ~/.J.4.R.V.1.5/80_bin
end

function j4tmp
    cd ~/.J.4.R.V.1.5/90_tmp
end

function j4archive
    cd ~/.J.4.R.V.1.5/99_archive
end

# ============================================
# COMANDOS DE STATUS E VALIDAÇÃO
# ============================================

function j4status
    echo "🏗️ J4RV15 v7.0.0 - Brutalist Purist Structure"
    echo "📍 Root: ~/.J.4.R.V.1.5"
    echo ""
    echo "📊 Estatísticas:"
    set dirs (ls -d ~/.J.4.R.V.1.5/*/ 2>/dev/null | wc -l)
    set files (find ~/.J.4.R.V.1.5 -type f 2>/dev/null | wc -l)
    echo "  • Diretórios canônicos: $dirs"
    echo "  • Total de arquivos: $files"
    echo ""
    echo "🔐 60_secrets:"
    if test -d ~/.J.4.R.V.1.5/60_secrets
        set perms (stat -c %a ~/.J.4.R.V.1.5/60_secrets)
        if test "$perms" = "700"
            echo "  ✅ Permissões corretas (700)"
        else
            echo "  ❌ Permissões incorretas ($perms)"
        end
    else
        echo "  ⚠️ Não encontrado"
    end
end

function j4tree
    echo "🌳 J4RV15 Directory Tree:"
    tree -L 2 -a ~/.J.4.R.V.1.5/ --dirsfirst
end

function j4tree-simple
    echo "📁 ~/.J.4.R.V.1.5/"
    for dir in (ls -d ~/.J.4.R.V.1.5/*/)
        echo "├── "(basename $dir)"/"
    end
end

function j4validate
    if test -f ~/.J.4.R.V.1.5/01_saas_foundry/tools/j4rv15_validate.py
        python3 ~/.J.4.R.V.1.5/01_saas_foundry/tools/j4rv15_validate.py
    else
        echo "❌ Script de validação não encontrado"
    end
end

# ============================================
# GERENCIAMENTO DE SECRETS
# ============================================

function j4secrets-init
    echo "🔐 Inicializando 60_secrets..."
    mkdir -p ~/.J.4.R.V.1.5/60_secrets/{.ssh,.gpg,.env.d,.tokens,.certs,.keys,.2fa,.vault}
    chmod 700 ~/.J.4.R.V.1.5/60_secrets
    chmod 700 ~/.J.4.R.V.1.5/60_secrets/.*
    touch ~/.J.4.R.V.1.5/60_secrets/.env
    chmod 600 ~/.J.4.R.V.1.5/60_secrets/.env
    echo "✅ 60_secrets inicializado com permissões seguras"
end

function j4env
    if test -f ~/.J.4.R.V.1.5/60_secrets/.env
        echo "📋 Carregando variáveis de ambiente..."
        for line in (grep -v '^#' ~/.J.4.R.V.1.5/60_secrets/.env | grep '=')
            set -gx (echo $line | cut -d'=' -f1) (echo $line | cut -d'=' -f2-)
        end
        echo "✅ Variáveis carregadas"
    else
        echo "❌ .env não encontrado"
    end
end

# ============================================
# BACKUP E RESTORE
# ============================================

function j4backup
    set backup_name "j4rv15_backup_"(date +%Y%m%d_%H%M%S)".tar.gz"
    set backup_path ~/.J.4.R.V.1.5/99_archive/backup/$backup_name
    
    mkdir -p ~/.J.4.R.V.1.5/99_archive/backup
    
    echo "📦 Criando backup: $backup_name"
    tar -czf $backup_path \
        --exclude='*.cache' \
        --exclude='*__pycache__*' \
        --exclude='*/90_tmp/*' \
        -C ~ .J.4.R.V.1.5
    
    echo "✅ Backup criado: $backup_path"
    echo "   Tamanho: "(du -h $backup_path | cut -f1)
end

function j4restore
    if test (count $argv) -eq 0
        echo "Uso: j4restore <arquivo_backup>"
        return 1
    end
    
    set backup_file $argv[1]
    
    if not test -f $backup_file
        echo "❌ Arquivo não encontrado: $backup_file"
        return 1
    end
    
    echo "⚠️ AVISO: Isso substituirá a estrutura atual!"
    read -P "Continuar? (yes/no): " confirm
    
    if test "$confirm" = "yes"
        echo "📦 Restaurando de $backup_file..."
        tar -xzf $backup_file -C ~
        echo "✅ Restauração completa"
    else
        echo "❌ Restauração cancelada"
    end
end

# ============================================
# AJUDA E DOCUMENTAÇÃO
# ============================================

function j4help
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    J4RV15 v7.0.0 - BRUTALIST PURIST COMMANDS                ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📁 NAVEGAÇÃO:"
    echo "  j4          → ~/.J.4.R.V.1.5/ (root)"
    echo "  j4local     → 00_.local/"
    echo "  j4logs      → 00_logs/"
    echo "  j4saas      → 01_saas_foundry/"
    echo "  j4tools     → 01_saas_foundry/tools/"
    echo "  j4configs   → 10_configs/"
    echo "  j4workspace → 20_workspace/"
    echo "  j4knowledge → 30_knowledge/"
    echo "  j4infra     → 40_infrastructure/"
    echo "  j4templates → 50_templates/"
    echo "  j4secrets   → 60_secrets/"
    echo "  j4media     → 70_media/"
    echo "  j4bin       → 80_bin/"
    echo "  j4tmp       → 90_tmp/"
    echo "  j4archive   → 99_archive/"
    echo ""
    echo "🔍 STATUS:"
    echo "  j4status    → Ver status do sistema"
    echo "  j4tree      → Visualizar árvore de diretórios"
    echo "  j4validate  → Validar estrutura"
    echo ""
    echo "🔐 SECRETS:"
    echo "  j4secrets-init → Inicializar 60_secrets"
    echo "  j4env          → Carregar .env"
    echo ""
    echo "💾 BACKUP:"
    echo "  j4backup    → Criar backup"
    echo "  j4restore   → Restaurar backup"
    echo ""
    echo "📖 AJUDA:"
    echo "  j4help      → Mostrar esta ajuda"
    echo ""
    echo "🧱 Filosofia: "Explícito sobre implícito. Direto sobre abstrato.""
end

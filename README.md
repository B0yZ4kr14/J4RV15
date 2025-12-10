# .J.4.R.V.1.5. v7.0.0 - Estrutura Brutalist Purist

## 🏗️ Filosofia e Implementação

Esta versão 7.0.0 do ecossistema **.J.4.R.V.1.5.** adota e implementa rigorosamente a filosofia **Brutalist Purist**, conforme definido na especificação v2.1.1. A estrutura de diretórios é explícita, hierárquica e determinística, com um forte foco em segurança e auditabilidade. Todas as correções de segurança identificadas na análise Popperiana foram aplicadas, resultando em um sistema robusto e transparente.

> "Explícito sobre implícito. Direto sobre abstrato. Transparente sobre mágico."

---

## 📁 Estrutura Canônica v7.0.0

A estrutura de diretórios é a espinha dorsal do sistema, impondo ordem e previsibilidade. Todos os componentes do ecossistema agora residem sob a raiz `~/.J.4.R.V.1.5/`.

```
~/.J.4.R.V.1.5/                      # Raiz do sistema (com pontos)
├── 00_.local/                       # Dados locais (XDG-Style)
├── 00_logs/                         # Logs e trilhas de auditoria
├── 01_saas_foundry/                 # Código-fonte, projetos e ferramentas
│   └── tools/                       # Scripts e agentes do .J.4.R.V.1.5.
├── 10_configs/                      # Arquivos de configuração de aplicações
├── 20_workspace/                    # Espaço de trabalho para projetos ativos
├── 30_knowledge/                    # Base de conhecimento e documentação
├── 40_infrastructure/               # Código de Infraestrutura como Código (IaC)
├── 50_templates/                    # Templates de código, configs e docs
├── 60_secrets/                      # Diretório seguro para todos os segredos (permissão 0700)
│   ├── .password-store/             # Raiz do 'pass' (Unix Password Store)
│   ├── .ssh/                        # Chaves SSH (0700)
│   ├── .gpg/                        # Chaves GPG (0700)
│   └── .env                         # Arquivo .env principal (0600)
├── 70_media/                        # Arquivos de mídia
├── 80_bin/                          # Binários e executáveis customizados
├── 90_tmp/                          # Arquivos temporários
└── 99_archive/                      # Arquivos e backups
```

---

## 🔐 Gestão de Segredos com `pass` na Estrutura Brutalist

A versão 7.0.0 integra o **SecretManagerAgent** e o **Unix Password Store (`pass`)** diretamente na estrutura Brutalist, garantindo uma gestão de segredos centralizada, segura e auditável.

- **Localização Central**: O cofre do `pass` (`~/.password-store`) é inicializado dentro do diretório seguro `~/.J.4.R.V.1.5/60_secrets/`. Isso garante que todos os segredos, gerenciados ou não pelo `pass`, estejam contidos na mesma estrutura segura e auditável.
- **Permissões Rigorosas**: O diretório `60_secrets/` e todos os seus subdiretórios (incluindo `.password-store/`) são mantidos com permissão `0700`, enquanto arquivos de segredos individuais são `0600`. O `umask 077` é aplicado globalmente pelo script de instalação para garantir a criação segura de novos arquivos.
- **SecretManagerAgent**: O agente foi atualizado para operar sobre o cofre do `pass` localizado em `~/.J.4.R.V.1.5/60_secrets/.password-store/`, abstraindo as operações de `store`, `retrieve`, `list`, `delete` e `rotate`.
- **Auditoria**: O script `j4rv15_audit.sh` foi aprimorado para validar a estrutura Brutalist, verificar as permissões do diretório `60_secrets/` e auditar o uso do `pass`.

---

## 🚀 Instalação e Configuração

O processo de instalação foi simplificado e automatizado através do script `install.sh`.

```bash
# 1. Conceder permissão de execução
chmod +x install.sh

# 2. Executar o instalador
./install.sh
```

O script irá:
1.  Instalar dependências Python (`rich`, `psutil`).
2.  Criar a estrutura de diretórios Brutalist completa em `~/.J.4.R.V.1.5/`.
3.  Copiar as funções Fish para `~/.config/fish/conf.d/j4rv15.fish`.
4.  Instalar o serviço de monitoramento do systemd em `~/.config/systemd/user/`.
5.  Validar a instalação e as permissões.

Após a instalação, é necessário inicializar o `pass`:

```fish
# 1. Identifique seu GPG ID
gpg --list-secret-keys --keyid-format LONG

# 2. Inicialize o pass DENTRO do diretório de segredos
pass init --path ~/.J.4.R.V.1.5/60_secrets/.password-store <SEU_GPG_ID>
```

---

## 🐟 Comandos Fish

Um conjunto de funções `fish` está disponível para navegação e gerenciamento rápidos:

- **Navegação**: `j4`, `j4logs`, `j4saas`, `j4configs`, `j4secrets`, etc.
- **Status e Validação**: `j4status`, `j4tree`, `j4validate`.
- **Gestão de Segredos**: `j4secrets-init`, `j4env`.
- **Backup**: `j4backup`, `j4restore`.
- **Ajuda**: `j4help` para ver todos os comandos.

Para carregar os comandos, execute: `source ~/.config/fish/conf.d/j4rv15.fish`

---

## 🛡️ Destaques de Segurança (Análise Popperiana)

- **Prevenção de TOCTOU**: Uso de file descriptors e locks atômicos para evitar race conditions.
- **Prevenção de Path Traversal**: Validação rigorosa de caminhos para garantir que as operações ocorram dentro da raiz `~/.J.4.R.V.1.5/`.
- **Operações Atômicas**: Todas as escritas de arquivos críticos são feitas de forma atômica (escrita em arquivo temporário e `rename`).
- **Permissões Seguras**: `umask 077` global, `60_secrets/` com `0700` e arquivos de segredos com `0600`.
- **Hardening de Systemd**: O serviço `j4rv15.service` possui um score de segurança aprimorado com diretivas como `NoNewPrivileges`, `ProtectSystem=strict` e `ProtectHome=read-only`.

---

## 📦 Conteúdo do Repositório

- **`README.md`**: Este documento.
- **`install.sh`**: Script de instalação automatizado.
- **`docs/`**: Documentação aprimorada, incluindo `SECRET_MANAGER_AGENT.md` e `PASS_MIGRATION_TUTORIAL.md` adaptados para a v7.0.0.
- **`scripts/`**: Contém o `j4rv15_brutalist.py` (core da estrutura), `secret_manager_agent.py` e `j4rv15_audit.sh`.
- **`fish/`**: Funções e aliases para o shell Fish.
- **`systemd/`**: Definição do serviço de monitoramento.

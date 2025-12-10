# Documentação Completa do Agente Gestor de Secrets .J.4.R.V.1.5.

## 1. Visão Geral e Filosofia

O **Agente Gestor de Secrets** é um componente central do ecossistema `.J.4.R.V.1.5.`, projetado para ser a autoridade máxima na gestão, auditoria e segurança de todos os segredos do sistema. Sua filosofia é baseada nos princípios de **segurança por padrão**, **mínimo privilégio** e **automação auditável**.

Este agente opera sob a premissa de que a gestão de segredos deve ser centralizada, padronizada e integrada a um backend criptográfico robusto, neste caso, o **GnuPG** através da interface do **`pass`** (passwordstore.org).

## 2. Arquitetura e Responsabilidades

O agente é responsável por um conjunto de tarefas críticas que garantem a integridade e a segurança do diretório canônico de segredos: `~/.J.4.R.V.1.5/60_secrets`.

### Responsabilidades Principais

| Responsabilidade | Descrição |
| :--- | :--- |
| **Auditoria Completa** | Realiza uma varredura completa da árvore de diretórios `60_secrets`, verificando a estrutura, permissões e consistência dos arquivos. |
| **Normalização de Permissões** | Garante que todos os diretórios e arquivos dentro da árvore de segredos sigam uma política de permissões estrita (ex: `700` para diretórios, `600` para arquivos). |
| **Detecção de Inconsistências** | Identifica segredos órfãos, formatos de arquivo inesperados, permissões incorretas e outras anomalias. |
| **Migração para `pass`** | Orquestra a migração completa de segredos de formatos legados (`.env`, `.passwords`, `.tokens`) para o cofre do `pass`. |
| **Geração de Scripts POSIX** | Produz scripts de auditoria e diagnóstico que são seguros, não destrutivos e compatíveis com `/bin/sh`. |
| **Integração com GPG** | Garante que o `pass` esteja corretamente configurado para usar as chaves GPG do usuário, localizadas em `~/.gnupg`. |

## 3. Estrutura do Diretório de Segredos

O agente opera exclusivamente dentro da seguinte estrutura de diretórios, considerada canônica:

```
~/.J.4.R.V.1.5/60_secrets/
├── .certificates/   # Certificados SSL/TLS
├── .env             # Arquivo de ambiente principal (legado, a ser migrado)
├── .env.d/          # Diretório para múltiplos arquivos .env (legado)
├── .gpg/            # Chaves GPG (link simbólico para ~/.gnupg)
├── .keys/           # Chaves de API e outros tokens brutos (legado)
├── .passwords/      # Senhas em texto plano (legado, crítico para migração)
├── .tokens/         # Tokens de autenticação (legado)
└── .ssh/            # Chaves SSH (link simbólico para ~/.ssh)
```

> **Nota Importante**: O uso de KeepassXC está obsoleto e foi completamente removido do ecossistema. Nenhuma referência a ele deve ser feita.

## 4. Interação com o Ambiente do Usuário

O agente é projetado para operar em um ambiente de usuário específico, caracterizado por:

- **Shell**: `fish`
- **Inicialização do Ambiente Gráfico**: Via TTY, sem gerenciador de login gráfico.
- **Ambientes Gráficos Suportados**: Hyprland (Wayland), XFCE4 (X11), GNOME (Wayland/X11).

O agente deve ser capaz de detectar o ambiente em execução para fornecer instruções e scripts compatíveis.

## 5. Fluxo de Migração para `pass`

O processo de migração é uma das responsabilidades mais críticas do agente. Ele segue um fluxo de trabalho estruturado para garantir uma transição segura e completa.

1.  **Instalação e Configuração**: O agente garante que `pass` e `gnupg` estejam instalados e que o `pass` seja inicializado com a chave GPG correta do usuário.
2.  **Vinculação de Chaves**: O diretório `~/.J.4.R.V.1.5/60_secrets/.gpg` é tratado como um link simbólico para `~/.gnupg`, garantindo que o sistema GPG do usuário seja a única fonte de verdade.
3.  **Importação de Segredos**: O agente lê os segredos dos diretórios legados (`.env`, `.passwords`, `.tokens`) e os importa para o cofre do `pass`, utilizando uma hierarquia de nomenclatura padronizada.
    - Exemplo: Uma chave de API da OpenAI em `.keys/openai.key` seria migrada para `pass J4RV15/api/openai`.
4.  **Verificação e Limpeza**: Após a migração, o agente verifica se todos os segredos foram importados corretamente e, em seguida, move os arquivos legados para um diretório de backup (`.migrated_secrets/`) antes de sugerir sua remoção segura.

## 6. Scripts de Auditoria

Quando solicitado, o agente gera um script de auditoria POSIX (`/bin/sh`) que realiza uma análise não destrutiva do sistema. O script gera um relatório detalhado em um arquivo de log com timestamp, como `~/J4RV15_audit_20260101_153344.txt`.

### Informações Coletadas pelo Script de Auditoria

- **Hardware**: CPU, GPU, RAM, Discos.
- **Pacotes**: Lista de pacotes instalados (específico do Arch Linux).
- **Serviços**: Status dos principais serviços (`systemd`).
- **Estrutura de Segredos**: Validação da árvore de diretórios `60_secrets`.
- **Permissões**: Verificação das permissões de arquivos e diretórios sensíveis.
- **Inconsistências**: Detecção de arquivos inesperados ou órfãos.
- **Ambiente Gráfico**: Identificação do ambiente gráfico em execução.
- **Integração GPG**: Verificação da configuração do GPG e do `pass`.

> **Segurança**: O script de auditoria **NUNCA** exibe o conteúdo de nenhum segredo no log ou na saída padrão.

---

**Versão**: 5.0.0  
**Data**: Dezembro 2024  
**Autor**: B0.y_Z4kr14

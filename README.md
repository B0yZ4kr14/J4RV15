# .J.4.R.V.1.5. - Plataforma Axiomatic de Orquestração Multi-LLM

> **Versão 3.0.0** | **Autor**: B0.y_Z4kr14 | **Licença**: MIT

---

## 🚀 Visão Geral

O **".J.4.R.V.1.5."** é uma plataforma sofisticada de orquestração de múltiplos provedores de LLM (Large Language Models) integrada com automação de fluxos de trabalho, inferência local, e observabilidade em nível empresarial. O sistema é projetado para ser operado exclusivamente via linha de comando (CLI), com uma rica suíte de comandos `j4*`, e se integra perfeitamente com as principais IDEs de desenvolvimento do mercado.

### ✨ Características Principais

| Característica | Descrição |
| :--- | :--- |
| **Multi-LLM Orchestration** | Acesso simultâneo a Anthropic, OpenAI, Google, Groq, OpenRouter e mais. |
| **Modo Híbrido** | Combinação inteligente de modelos locais (via Ollama) com APIs em nuvem. |
| **IDE-Agnostic** | Integração nativa com VSCode, Antigravity, Claude Desktop, Cursor e Windsurf. |
| **CLI-First** | Interface de linha de comando completa com comandos `j4*` para todas as operações. |
| **Modular & Atômico** | Arquitetura baseada em agentes atômicos reutilizáveis e descentralizados. |
| **Enterprise-Grade** | Observabilidade com Prometheus/Grafana, logging estruturado e segurança OWASP. |

---

## 🛠️ Arquitetura e Documentação

Para uma compreensão aprofundada da arquitetura, requisitos e plano de desenvolvimento, consulte os seguintes documentos:

1.  **[📄 Especificação Técnica Completa](./SPECIFICATION_J4RV15.md)**: Detalha todos os requisitos, módulos, arquitetura da aplicação, estrutura de diretórios, sistema de comandos e o ecossistema de agentes.

2.  **[🗺️ Plano de Implementação Segmentado](./IMPLEMENTATION_PLAN.md)**: Apresenta o plano de desenvolvimento dividido em fases e módulos atômicos, projetado para ser seguido por um agente de IA, garantindo uma implementação modular e sem perda de contexto.

---

## 📦 Estrutura do Projeto

O projeto está organizado em uma estrutura de diretórios modular e lógica, projetada para máxima clareza e manutenibilidade. A estrutura completa pode ser encontrada na [Especificação Técnica](./SPECIFICATION_J4RV15.md).

```
~/.J.4.R.V.1.5/
├── 01_saas_foundry/            # Core do sistema (código-fonte, ferramentas, docs)
├── 10_configs/                 # Configurações centralizadas (LiteLLM, Grafana, IDEs, Shell)
├── 60_secrets/                 # Segredos criptografados (NUNCA commitar)
├── 70_python/                  # Ambientes e dependências Python
├── docker-compose.yml          # Stack de serviços Docker
└── README.md                   # Este arquivo
```

---

## ⚙️ Instalação Rápida

O processo de instalação é totalmente automatizado pelo script principal, que cuida da detecção de ambiente, instalação de dependências, configuração de serviços e integração de credenciais.

**Pré-requisitos:**

1.  Coloque os arquivos `id_ed25519`, `id_ed25519.pub` e `.env.J.4.R.V.1.5` no diretório de instalação (ex: `~/Documents/j4rv15/Install`).
2.  Certifique-se de ter Python 3.8+ e Docker 24.0+ instalados.

**Execução:**

```bash
# Navegue até o diretório do projeto clonado
cd /path/to/J4RV15

# Execute o instalador principal (que será criado na Fase 8)
python3 j4rv15_installer.py --env ~/Documents/j4rv15/Install/.env.J.4.R.V.1.5 --auto
```

O instalador irá guiá-lo através dos modos de instalação (`offline`, `hybrid`, `openrouter`) e da seleção de IDE.

---

## 命令行 (CLI)

O sistema é controlado por um conjunto de comandos `j4*`:

| Comando | Descrição |
| :--- | :--- |
| `j4 fix` | Analisa e corrige toda a estrutura de arquivos, tokens, configurações, etc. |
| `j4 validate` | Valida o ambiente de execução e as dependências. |
| `j4 install` | Inicia o processo de instalação e setup. |
| `j4 update` | Atualiza LLMs, dependências e ferramentas. |
| `j4 wizard` | Abre o assistente interativo para configuração e seleção de modo. |
| `j4 ide` | Gerencia a integração e configuração das IDEs. |
| `j4 secrets` | Gerencia chaves, tokens e credenciais de forma segura. |
| `j4 docker` | Controla a stack de serviços do Docker. |
| `j4 health` | Realiza uma verificação completa da saúde do sistema. |
| `j4 help` | Exibe a ajuda para todos os comandos. |

---

## 🎯 Próximos Passos

O desenvolvimento seguirá o [Plano de Implementação](./IMPLEMENTATION_PLAN.md) detalhado, começando pela criação dos scripts do core do sistema e da CLI.

1.  **Desenvolver o Core do Sistema**: Scripts para detecção de ambiente, gestão de arquivos e CLI.
2.  **Implementar a Stack Docker**: Refatorar e automatizar o `docker-compose`.
3.  **Configurar o Gateway de LLMs**: Gerar dinamicamente a configuração do LiteLLM.
4.  **Construir o Ecossistema de Agentes**: Desenvolver os agentes atômicos modulares.
5.  **Finalizar o Instalador**: Unir todos os módulos no script `j4rv15_installer.py`.

---

> Este projeto é um trabalho em andamento. A documentação e o código serão continuamente refinados e aprimorados.

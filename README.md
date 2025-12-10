# .J.4.R.V.1.5. - Sistema de Orquestração de Ambiente de Desenvolvimento

**Versão**: 3.8.0 | **Autor**: B0.y_Z4kr14 | **Data**: Dezembro 2024

---

## 🎯 Visão Geral

O **.J.4.R.V.1.5.** é um sistema de orquestração de ambiente de desenvolvimento projetado para ser **modular, descentralizado e híbrido**. Ele automatiza a configuração, validação e manutenção de ambientes de desenvolvimento complexos, com foco em segurança, automação e integração.

## ✨ Princípios de Design

- **Modularidade**: Cada componente é um agente atômico e independente.
- **Descentralização**: Não há um ponto único de falha.
- **Segurança**: Gestão de credenciais e chaves com criptografia forte.
- **Automação**: Scripts para validação, limpeza e manutenção.
- **Integração**: Suporte para múltiplas IDEs, LLMs e serviços.

## 🚀 Primeiros Passos: Guia Rápido

| Passo | Ação | Comando |
| :--- | :--- | :--- |
| 1. 📂 | Clone o repositório | `git clone https://github.com/B0yZ4kr14/J4RV15.git` |
| 2. 🔑 | Prepare suas credenciais | `mv id_ed25519* .env.J.4.R.V.1.5 J4RV15/config/` |
| 3. 🛠️ | Execute o instalador | `cd J4RV15 && python3 j4rv15_installer.py --auto` |
| 4. ✨ | Comece a usar! | `j4 help` |

### 🎮 Experimente Agora! (Sem Instalação)

Quer testar o `.J.4.R.V.1.5.` sem instalar nada? Acesse nosso playground interativo e comece a usar em segundos:

[▶️ Iniciar Playground Interativo](https://www.katacoda.com/your-scenario)

## 🤖 Ecossistema de Agentes Atômicos

| Agente | Responsabilidade |
| :--- | :--- |
| **SystemDetectorAgent** | Coleta inventário de hardware, software e rede. |
| **SecurityAgent** | Gerencia o ciclo de vida de credenciais e chaves. |
| **LLMManagerAgent** | Gerencia o ciclo de vida de modelos de linguagem. |
| **EnvironmentValidatorAgent** | Valida dependências e configurações. |
| **MonitoringAgent** | Realiza verificações de saúde nos serviços. |
| **ConfigurationAgent** | Gerencia a configuração dinâmica do sistema. |

## ⚙️ Fluxo de Trabalho do ConfigurationAgent

```mermaid
graph TD
    A[Início] --> B{j4 config [comando]};
    B --> C{Comando é \'get\'}?;
    C -- Sim --> D[Chama ConfigurationAgent.get(key)];
    D --> E{Arquivo de Configuração Existe?};
    E -- Sim --> F[Lê YAML/JSON/INI];
    F --> G[Retorna Valor];
    E -- Não --> H[Retorna Nulo];
    C -- Não --> I{Comando é \'set\'}?;
    I -- Sim --> J[Chama ConfigurationAgent.set(key, value)];
    J --> K{Arquivo de Configuração Existe?};
    K -- Sim --> L[Lê YAML/JSON/INI];
    L --> M[Atualiza/Adiciona Valor];
    M --> N[Salva Arquivo];
    N --> O[Retorna Status de Sucesso];
    K -- Não --> P[Cria Novo Dicionário de Configuração];
    P --> M;
    I -- Não --> Q[Comando Inválido];
    Q --> R[Retorna Mensagem de Erro];
    G --> S[Fim];
    H --> S;
    O --> S;
    R --> S;
```

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia o arquivo `CONTRIBUTING.md` para mais detalhes.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

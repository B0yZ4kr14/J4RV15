# Documentação do Fluxo de Trabalho do Módulo `j4fix`

> **Versão 1.0** | **Autor**: B0.y_Z4kr14 | **Data**: Dezembro 2024

---

## 1. Visão Geral

O diagrama de fluxo de trabalho do `j4fix` ilustra a sequência de operações executadas pelo `J4FixOrchestrator` quando o comando `j4 fix` é invocado pelo usuário. O objetivo deste workflow é realizar uma análise completa e sistemática do ambiente `.J.4.R.V.1.5.`, identificar problemas e sugerir correções acionáveis.

O fluxo é condicional e depende da flag `--full-scan`, permitindo tanto uma verificação rápida quanto uma análise profunda.

## 2. Fases do Fluxo de Trabalho

### Fase 1: Iniciação e Análise do Sistema

1.  **Entrada do Usuário**: O processo começa com o usuário executando `j4 fix`, opcionalmente com a flag `--full-scan`.
2.  **Orquestrador**: O `J4FixOrchestrator` é inicializado.
3.  **Decisão de Scan**: O orquestrador verifica a presença da flag `--full-scan`.
4.  **Execução do `SystemDetectorAgent`**: 
    -   **Scan Completo**: Coleta informações detalhadas de hardware, SO, rede e shell.
    -   **Scan Rápido**: Coleta apenas informações essenciais.
5.  **Resultado**: O agente retorna um `system_context` detalhado.

### Fase 2: Validação do Ambiente

1.  **Execução do `EnvironmentValidatorAgent`**: Este agente utiliza o `system_context` para validar componentes críticos.
2.  **Verificações Sequenciais**:
    -   `validate_docker`: Verifica se o Docker está instalado e em execução.
    -   `validate_python`: Garante que a versão do Python é compatível (>= 3.9).
    -   `validate_git`: Confirma a instalação do Git.
    -   `validate_permissions`: Checa se o usuário tem as permissões necessárias.
    -   `validate_network`: Testa a conectividade com a internet.
3.  **Resultado**: O agente retorna `validation_results` com o status de cada verificação.

### Fase 3: Auditoria de Segurança

1.  **Execução do `SecurityAgent`**: Realiza uma auditoria de segurança.
2.  **Verificações de Segurança**:
    -   `check_ssh_keys`: Valida a existência e as permissões das chaves SSH.
    -   `check_api_tokens`: Verifica se os tokens de API estão devidamente criptografados.
3.  **Resultado**: O agente retorna `security_results`.

### Fase 4: Manutenção e Limpeza (Apenas em Scan Completo)

1.  **Execução do `MaintenanceAgent`**: Se `--full-scan` estiver ativo, este agente verifica a necessidade de limpeza.
2.  **Verificações de Manutenção**:
    -   `check_docker_prune`: Identifica imagens, contêineres e volumes Docker não utilizados.
    -   `check_log_files`: Procura por arquivos de log antigos que podem ser arquivados.
    -   `check_cache_files`: Verifica caches obsoletos.
3.  **Resultado**: O agente retorna `maintenance_results` com recomendações.

### Fase 5: Monitoramento de Saúde

1.  **Execução do `MonitoringAgent`**: Verifica a saúde de todos os serviços ativos.
2.  **Verificações de Saúde**:
    -   `check_postgres`: Testa a conexão com o banco de dados.
    -   `check_ollama`: Verifica se o serviço Ollama está respondendo.
    -   `check_litellm`: Testa o gateway do LiteLLM.
    -   `check_mcp_servers`: Valida os servidores MCP.
3.  **Resultado**: O agente retorna `health_results` com o status de cada componente.

### Fase 6: Agregação e Geração do Relatório

1.  **Agregação**: O `J4FixOrchestrator` coleta os resultados de todos os agentes executados.
2.  **Geração do Sumário**: O método `_generate_summary` é chamado para consolidar as descobertas.
3.  **Análise de Problemas**: O orquestrador calcula o número total de problemas (`total_issues`) e sugestões (`total_suggestions`).
4.  **Status Final**: Define o `overall_status` como "OK" ou "NEEDS_ATTENTION".
5.  **Formatação**: O relatório final é formatado em uma estrutura JSON clara.
6.  **Saída**: O relatório é exibido para o usuário no terminal.

## 3. Legenda de Cores do Diagrama

-   **Azul Claro**: Entrada do usuário.
-   **Verde Claro**: Fim do workflow (sucesso).
-   **Amarelo**: Agente de Segurança.
-   **Roxo**: Agente de Detecção do Sistema.
-   **Laranja**: Agente de Validação do Ambiente.
-   **Rosa**: Agente de Monitoramento.
-   **Verde-Limão**: Agente de Manutenção.

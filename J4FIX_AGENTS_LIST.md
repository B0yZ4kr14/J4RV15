# Agentes Atômicos Envolvidos no Fluxo de Trabalho do `j4fix`

O fluxo de trabalho do `j4fix` orquestra uma série de agentes atômicos, cada um com uma responsabilidade específica, para garantir uma análise completa e precisa do sistema. Abaixo estão listados os agentes envolvidos e suas funções.

| Agente | Função Breve |
| :--- | :--- |
| **SystemDetectorAgent** | Coleta informações detalhadas sobre o hardware (CPU, GPU, RAM, disco), sistema operacional (distribuição, kernel), rede (IPs, DNS, velocidade) e ambiente de shell (Bash, Zsh, etc.). |
| **EnvironmentValidatorAgent** | Verifica se todas as dependências críticas do sistema, como Docker, Python e Git, estão instaladas, configuradas e em execução corretamente. |
| **SecurityAgent** | Realiza uma auditoria de segurança, verificando a existência e as permissões corretas das chaves SSH e garantindo que os tokens de API estejam devidamente criptografados. |
| **MaintenanceAgent** | (Executado apenas com `--full-scan`) Procura por oportunidades de limpeza, como imagens Docker não utilizadas, logs antigos e caches obsoletos, sugerindo ações para liberar espaço e organizar o sistema. |
| **MonitoringAgent** | Verifica a saúde e o status operacional de todos os serviços e componentes vitais do `.J.4.R.V.1.5.`, incluindo o banco de dados PostgreSQL, o serviço Ollama, o gateway LiteLLM e os servidores MCP. |

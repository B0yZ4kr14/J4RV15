# Documentação Detalhada: ConfigurationAgent

**Responsabilidade**: Gerenciar a configuração dinâmica do sistema `.J.4.R.V.1.5.`, permitindo que os usuários personalizem o comportamento dos agentes, modelos e ferramentas através de uma interface de linha de comando (`j4 config`).

**Prompt de Exemplo**:
```json
{
  "task": {
    "action": "set_config",
    "key": "llm.default_model",
    "value": "llama3.2"
  },
  "description": "Defina o modelo de linguagem padrão para ser 'llama3.2'."
}
```

**Saída Esperada**:
```json
{
  "status": "SUCCESS",
  "key": "llm.default_model",
  "old_value": "qwen2.5-coder",
  "new_value": "llama3.2"
}
```

**Ferramentas Utilizadas**:

| Tipo | Ferramenta | Propósito |
| :--- | :--- | :--- |
| **Python** | `yaml` | Ler e escrever arquivos de configuração YAML. |
| | `json` | Ler e escrever arquivos de configuração JSON. |
| | `configparser` | Ler e escrever arquivos de configuração INI. |
| **Shell** | `j4` | Interface de linha de comando para interagir com o agente. |

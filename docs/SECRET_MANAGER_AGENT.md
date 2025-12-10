# SecretManagerAgent v1.0 - Documentação Técnica

## 1. Visão Geral e Integração com a Estrutura Brutalist

O **SecretManagerAgent** é o sétimo agente atômico do ecossistema **.J.4.R.V.1.5.** e serve como a interface programática para a gestão segura de segredos. Na versão 1.0, o agente foi totalmente adaptado para operar dentro da **Estrutura Core**, utilizando o **Unix Password Store (`pass`)** como backend de armazenamento seguro.

O agente agora opera exclusivamente sobre o cofre do `pass` localizado em `~/.J.4.R.V.1.5/60_secrets/.password-store/`, garantindo que todas as operações de segredos estejam centralizadas, criptografadas e em conformidade com as permissões rigorosas (`0700`) da estrutura.

---

## 2. Arquitetura e Funcionalidades

O agente mantém sua interface `run_task(task: dict)`, mas as operações internas foram refatoradas para interagir com o `pass` através de comandos de subprocesso.

### 2.1. Interface de Tarefas

O agente responde a um dicionário de tarefas com a seguinte estrutura:

```json
{
    "action": "<operação>",
    "name": "<nome_do_segredo>",
    "value": "<valor_do_segredo>", // Opcional
    "options": {} // Opcional
}
```

### 2.2. Operações Suportadas

| Ação | Descrição | Exemplo de `name` | `value` | `options` |
| :--- | :--- | :--- | :--- | :--- |
| `store` | Armazena um novo segredo ou atualiza um existente. | `J4RV15/api/openai` | Obrigatório | `{"multiline": true}` |
| `retrieve` | Recupera o valor de um segredo. | `J4RV15/api/openai` | Ignorado | `{"clip": true}` (copia para clipboard) |
| `list` | Lista segredos dentro de uma hierarquia. | `J4RV15/api` | Ignorado | `{}` |
| `delete` | Remove um segredo de forma segura. | `J4RV15/api/openai` | Ignorado | `{"force": true}` |
| `generate` | Gera uma nova senha segura. | `J4RV15/services/database` | Ignorado | `{"length": 32, "no-symbols": false}` |

### 2.3. Exemplo de Implementação Python (`secret_manager_agent.py`)

O código do agente foi adaptado para definir o `PASSWORD_STORE_DIR` e executar comandos `pass`.

```python
import subprocess
import os

class SecretManagerAgent:
    def __init__(self):
        self.password_store_dir = os.path.expanduser("~/.J.4.R.V.1.5/60_secrets/.password-store")
        self.env = os.environ.copy()
        self.env["PASSWORD_STORE_DIR"] = self.password_store_dir

    def _run_pass_command(self, args: list[str]) -> dict:
        try:
            process = subprocess.run(
                ["pass"] + args,
                capture_output=True,
                text=True,
                check=True,
                env=self.env
            )
            return {"status": "success", "output": process.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr.strip()}

    def run_task(self, task: dict) -> dict:
        action = task.get("action")
        name = task.get("name")

        if action == "retrieve":
            return self._run_pass_command([name])
        
        # ... outras ações ...
```

---

## 3. Integração com o Script de Auditoria (`j4rv15_audit.sh`)

O `SecretManagerAgent` é uma peça fundamental no ciclo de auditoria. O script `j4rv15_audit.sh` foi aprimorado para:

1.  **Verificar a Existência do Agente**: Confirma que `secret_manager_agent.py` existe em `~/.J.4.R.V.1.5/01_saas_foundry/tools/`.
2.  **Validar a Configuração do `pass`**: Executa verificações para garantir que o `PASSWORD_STORE_DIR` está configurado corretamente e que o cofre está inicializado.
3.  **Auditar Acessos (Futuro)**: A integração com os logs do `pass` (se configurado) permitirá ao agente analisar padrões de acesso e detectar anomalias, como um segredo sendo acessado com muita frequência ou de locais inesperados.

### Exemplo de Verificação no Script de Auditoria:

```bash
# ... dentro de j4rv15_audit.sh ...

PASSWORD_STORE_DIR="$HOME/.J.4.R.V.1.5/60_secrets/.password-store"

if [ ! -d "$PASSWORD_STORE_DIR" ]; then
    echo "{\"status\": \"ERROR\", \"check\": \"pass_store_existence\", \"message\": \"Diretório do pass não encontrado em $PASSWORD_STORE_DIR\"}"
fi

if [ ! -f "$PASSWORD_STORE_DIR/.gpg-id" ]; then
    echo "{\"status\": \"ERROR\", \"check\": \"pass_initialization\", \"message\": \"Cofre do pass não inicializado (arquivo .gpg-id não encontrado)\"}"
fi
```

---

## 4. Casos de Uso na Estrutura

### 4.1. Configuração de um Novo Serviço

1.  **Orquestrador** solicita ao **SecretManagerAgent** a geração de uma nova senha para um banco de dados.
    - `task = {"action": "generate", "name": "J4RV15/database/postgres", "options": {"length": 24}}`
2.  O **SecretManagerAgent** executa `pass generate J4RV15/database/postgres 24` e armazena a senha.
3.  O **Orquestrador** solicita ao **ConfigurationAgent** que crie um arquivo de configuração para o serviço, requisitando a senha ao **SecretManagerAgent**.
    - `db_password = secret_agent.run_task({"action": "retrieve", "name": "J4RV15/database/postgres"})`
4.  O **ConfigurationAgent** escreve o arquivo de configuração em `~/.J.4.R.V.1.5/10_configs/apps/postgres.conf` com a senha recuperada.

### 4.2. Rotação de uma Chave de API

1.  Um **Job Agendado** (via `systemd` ou `cron`) invoca o **SecretManagerAgent** com uma tarefa de rotação.
    - `task = {"action": "rotate", "name": "J4RV15/api/openai"}`
2.  O **SecretManagerAgent**:
    a.  Gera uma nova chave (usando `pass generate`).
    b.  Armazena a chave antiga em `J4RV15/api/openai.old`.
    c.  Insere a nova chave em `J4RV15/api/openai`.
    d.  (Opcional) Invoca um webhook ou script para atualizar o serviço externo com a nova chave.
3.  O agente registra a rotação em `~/.J.4.R.V.1.5/00_logs/audit/secrets.log`.

---

## 5. Conclusão

A versão 1.0 do **SecretManagerAgent** solidifica seu papel como o guardião dos segredos do ecossistema **.J.4.R.V.1.5.**. Ao se integrar perfeitamente com a **Estrutura Core** e o **Unix Password Store**, o agente oferece uma solução de gestão de segredos que é ao mesmo tempo robusta, segura, auditável e alinhada com a filosofia de transparência e explicitude do sistema.

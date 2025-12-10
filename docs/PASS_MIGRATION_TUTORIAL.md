# Tutorial de Migração para `pass` na Estrutura Brutalist v7.0.0

## 1. Introdução

Este tutorial descreve como inicializar e usar o `pass` (Unix Password Store) dentro da nova estrutura **Brutalist Purist** do ecossistema **.J.4.R.V.1.5.**, garantindo que a gestão de segredos esteja centralizada, segura e alinhada com a filosofia do sistema.

---

## 2. Pré-requisitos

- **Estrutura v7.0.0 Instalada**: O script `install.sh` deve ter sido executado, criando a estrutura de diretórios em `~/.J.4.R.V.1.5/`.
- **GnuPG Instalado**: O `gpg` deve estar instalado e uma chave GPG pessoal deve ter sido gerada.
- **`pass` Instalado**: O `pass` deve estar instalado no sistema (`sudo pacman -S pass` ou `sudo apt install pass`).

---

## 3. Fase 1: Inicialização do `pass` na Estrutura Correta

A principal mudança na v7.0.0 é a localização do cofre do `pass`. Ele agora reside **dentro** do diretório `60_secrets`.

### 3.1. Identificação da Chave GPG

Primeiro, obtenha o ID da sua chave GPG. Este ID será usado para criptografar todos os segredos.

```fish
gpg --list-secret-keys --keyid-format LONG
```

Copie o ID longo (ex: `4A4E424553534841`) da sua chave principal.

### 3.2. Inicialização do Cofre `pass`

Utilize o comando `pass init` com a flag `--path` para especificar a localização exata do cofre.

```fish
# Defina o caminho do cofre
set -x PASSWORD_STORE_DIR ~/.J.4.R.V.1.5/60_secrets/.password-store

# Inicialize o pass com seu GPG ID
pass init --path $PASSWORD_STORE_DIR <SEU_GPG_ID>
```

- **Explicação**: Este comando cria o diretório `~/.J.4.R.V.1.5/60_secrets/.password-store/`, o inicializa como um repositório Git e o configura para usar sua chave GPG. A variável de ambiente `PASSWORD_STORE_DIR` garante que todos os comandos `pass` subsequentes atuem neste diretório específico.

Para tornar esta configuração permanente, adicione a seguinte linha ao seu `~/.config/fish/config.fish`:

```fish
set -x PASSWORD_STORE_DIR ~/.J.4.R.V.1.5/60_secrets/.password-store
```

---

## 4. Fase 2: Migração e Uso de Segredos

Com o cofre inicializado, você pode começar a adicionar e gerenciar segredos.

### 4.1. Adicionando um Novo Segredo

Use o comando `pass insert` para adicionar um novo segredo. A estrutura hierárquica é recomendada.

```fish
# Adicionar uma chave de API
pass insert J4RV15/api/openai
```

O `pass` solicitará que você digite o segredo. Ele será então criptografado e salvo em `~/.J.4.R.V.1.5/60_secrets/.password-store/J4RV15/api/openai.gpg`.

### 4.2. Recuperando um Segredo

Para visualizar um segredo, use o comando `pass` seguido do nome do segredo.

```fish
# Exibir a chave de API do OpenAI
pass J4RV15/api/openai

# Copiar a chave para a área de transferência (clipboard)
pass -c J4RV15/api/openai
```

### 4.3. Migrando do `.env` Legado

Se você possui segredos em um arquivo `.env` legado, pode migrá-los com o seguinte script `fish`:

```fish
while read -r line
    if string match -q -r ".*=" $line
        set key (echo $line | cut -d= -f1)
        set value (echo $line | cut -d= -f2-)
        set pass_name "J4RV15/env/$(echo $key | tr '[:upper:]' '[:lower:]')"
        echo $value | pass insert -e $pass_name
    end
end < ~/.J.4.R.V.1.5/60_secrets/.env
```

- **Explicação**: Este script lê o arquivo `.env`, extrai cada par chave/valor e o insere no `pass` sob a hierarquia `J4RV15/env/`.

---

## 5. Fase 3: Validação de Integridade

Após a inicialização e migração, valide se a estrutura e os segredos estão corretos.

### 5.1. Verificação da Estrutura

Use o comando `pass` (ou `pass ls`) para listar todos os segredos no cofre.

```fish
pass
# ou
pass ls J4RV15
```

Isso deve exibir a árvore de segredos que você criou, confirmando que eles estão no local correto e foram criptografados.

### 5.2. Verificação com o Script de Auditoria

O script de auditoria da v7.0.0 foi aprimorado para verificar a configuração do `pass`.

```fish
# Navegue até o diretório de ferramentas
cd ~/.J.4.R.V.1.5/01_saas_foundry/tools

# Execute o script de auditoria
./j4rv15_audit.sh
```

O script irá verificar:
- Se o diretório `~/.J.4.R.V.1.5/60_secrets/.password-store` existe.
- Se as permissões do diretório `60_secrets` e seus subdiretórios estão corretas (`0700`).
- Se o `pass` está inicializado corretamente.

---

## 6. Conclusão

Ao seguir este tutorial, você terá configurado o `pass` de forma segura e integrada à estrutura Brutalist Purist v7.0.0. Todos os seus segredos estarão centralizados, criptografados com sua chave GPG e gerenciados por uma ferramenta padrão da indústria, ao mesmo tempo que se beneficiam da organização e segurança impostas pelo ecossistema **.J.4.R.V.1.5.**.

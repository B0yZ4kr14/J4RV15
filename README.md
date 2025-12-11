
# .J.4.R.V.1.5. v1.0 - Core Structure

![J4RV15 Banner](https://i.imgur.com/sC9m8pC.png)

## 🚀 Introdução

Bem-vindo ao **.J.4.R.V.1.5. v1.0**, um ecossistema de automação e gerenciamento de projetos projetado para ser seguro, organizado e determinístico. Esta plataforma fornece uma estrutura de diretórios hierárquica e um conjunto de ferramentas para centralizar configurações, segredos, logs e código-fonte, garantindo um ambiente de desenvolvimento e operações limpo e auditável.

A filosofia central do projeto é a simplicidade e a transparência, encapsulada pela citação:

> "A simplicidade é o último grau de sofisticação." - Leonardo da Vinci

Este `README.md` serve como o guia definitivo para a arquitetura, instalação, configuração e uso do ecossistema .J.4.R.V.1.5.

---


---

## 🏗️ Arquitetura e Filosofia

A arquitetura do .J.4.R.V.1.5. é baseada em três pilares fundamentais:

1.  **Estrutura Hierárquica Explícita**: Uma estrutura de diretórios numerada e previsível que elimina a ambiguidade e impõe a organização. Cada diretório tem um propósito claro, facilitando a localização de qualquer artefato.

2.  **Segurança por Padrão**: O sistema é projetado com a segurança em mente, não como um adendo. Isso se manifesta através de permissões de arquivo rigorosas, gerenciamento de segredos centralizado e criptografado, e scripts de auditoria integrados.

3.  **Automação Transparente**: As ferramentas fornecidas automatizam tarefas repetitivas (como criação de estrutura, backup e configuração), mas o fazem de forma transparente, com scripts legíveis e sem "mágica" oculta.

| Pilar | Descrição | Benefício Principal |
| :--- | :--- | :--- |
| **Estrutura** | Diretórios numerados de `00_` a `99_` com funções específicas. | **Previsibilidade**: Encontre qualquer arquivo ou configuração rapidamente. |
| **Segurança** | Integração nativa com GPG e `pass`, permissões `0700` para segredos. | **Confiança**: Segredos e dados sensíveis são protegidos por padrão. |
| **Automação** | Scripts para instalação, validação, backup e navegação. | **Eficiência**: Reduz o trabalho manual e o risco de erro humano. |

---

## 📁 Estrutura de Diretórios Canônica

A espinha dorsal do sistema é a sua estrutura de diretórios, localizada em `~/.J.4.R.V.1.5/`. Cada diretório é prefixado com um número que indica sua função e prioridade.

```
~/.J.4.R.V.1.5/
├── 00_.local/          # Dados locais (XDG-Style)
├── 00_logs/            # Logs e trilhas de auditoria
├── 01_saas_foundry/    # Código-fonte, projetos e ferramentas
│   └── tools/          # Scripts e agentes do .J.4.R.V.1.5.
├── 10_configs/         # Arquivos de configuração de aplicações
├── 20_workspace/       # Espaço de trabalho para projetos ativos
├── 30_knowledge/       # Base de conhecimento e documentação
├── 40_infrastructure/  # Código de Infraestrutura como Código (IaC)
├── 50_templates/       # Templates de código, configs e docs
├── 60_secrets/         # Diretório seguro para todos os segredos (permissão 0700)
│   ├── .password-store/  # Raiz do 'pass' (Unix Password Store)
│   ├── .ssh/           # Chaves SSH (0700)
│   └── .gpg/           # Chaves GPG (0700)
├── 70_media/           # Arquivos de mídia
├── 80_bin/             # Binários e executáveis customizados
├── 90_tmp/             # Arquivos temporários
└── 99_archive/         # Arquivos e backups
```

---

## 🚀 Instalação e Configuração

O processo de instalação é automatizado pelo script `install.sh`, que configura a estrutura de diretórios, instala dependências e configura as ferramentas.

### Pré-requisitos

-   **Sistema Operacional**: Linux (recomendado Ubuntu 22.04+) ou macOS.
-   **Shell**: `bash` e `fish` (recomendado).
-   **Ferramentas**: `git`, `python3`, `pip`, `gpg`, `pass`.

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/B0yZ4kr14/J4RV15.git
cd J4RV15
```

### Passo 2: Executar o Script de Instalação

O script `install.sh` irá criar a estrutura completa em `~/.J.4.R.V.1.5/`.

```bash
# Conceder permissão de execução
chmod +x install.sh

# Executar o instalador
./install.sh
```

O instalador irá:

1.  Verificar as dependências.
2.  Criar a estrutura de diretórios com as permissões corretas.
3.  Copiar as funções `fish` para `~/.config/fish/conf.d/`.
4.  Instalar o serviço `systemd` (se aplicável).
5.  Validar a instalação.

---

## 🔐 Gestão de Segredos com `pass`

A gestão de segredos é um componente crítico do ecossistema, e é centralizada no **Unix Password Store (`pass`)**, que utiliza GPG para criptografia.

### Passo 3: Configuração do GPG

Se você ainda não tem uma chave GPG, crie uma:

```bash
gpg --full-generate-key
```

Siga as instruções, selecionando RSA e um tamanho de chave de 4096 bits.

### Passo 4: Inicialização do `pass`

O cofre do `pass` deve ser inicializado **dentro** da estrutura do .J.4.R.V.1.5. para garantir que ele herde as permissões de segurança corretas.

1.  **Identifique sua Chave GPG**: Obtenha o ID longo da sua chave.

    ```fish
    gpg --list-secret-keys --keyid-format LONG
    ```

    Copie o ID da chave (ex: `3AA5C34371567BD2`).

2.  **Inicialize o Cofre**: Use o comando `pass init` com a flag `--path` para especificar a localização exata.

    ```fish
    # Defina a variável de ambiente para a sessão atual
    set -x PASSWORD_STORE_DIR ~/.J.4.R.V.1.5/60_secrets/.password-store

    # Inicialize o pass com seu GPG ID
    pass init --path $PASSWORD_STORE_DIR <SEU_GPG_ID>
    ```

3.  **Torne a Configuração Permanente**: Para que o `pass` sempre use este diretório, adicione a seguinte linha ao seu arquivo de configuração do shell (ex: `~/.config/fish/config.fish`):

    ```fish
    set -x PASSWORD_STORE_DIR ~/.J.4.R.V.1.5/60_secrets/.password-store
    ```

### Uso Básico do `pass`

-   **Adicionar um segredo**:

    ```bash
    pass insert J4RV15/api/openai
    ```

-   **Recuperar um segredo**:

    ```bash
    pass J4RV15/api/openai
    ```

-   **Copiar para a área de transferência**:

    ```bash
    pass -c J4RV15/api/openai
    ```

-   **Listar todos os segredos**:

    ```bash
    pass
    ```

---

## 🛠️ Ferramentas e Automação

O ecossistema inclui um conjunto de ferramentas para simplificar o gerenciamento.

### Funções Fish (`j4rv15.fish`)

Um conjunto de mais de 20 funções para o shell `fish` que facilitam a navegação e a execução de tarefas comuns. Após a instalação, execute `j4help` para ver todos os comandos disponíveis.

| Comando | Descrição |
| :--- | :--- |
| `j4` | Navega para a raiz `~/.J.4.R.V.1.5/`. |
| `j4secrets` | Navega diretamente para o diretório `60_secrets/`. |
| `j4status` | Exibe um resumo do status do sistema. |
| `j4tree` | Mostra a árvore de diretórios da estrutura. |
| `j4validate` | Executa o script de validação da estrutura. |
| `j4backup` | Cria um backup compactado de toda a estrutura. |
| `j4help` | Exibe a lista completa de comandos. |

### Scripts Principais

-   **`j4rv15_brutalist.py`**: O script Python que forma o núcleo da criação e validação da estrutura. Garante que todas as operações de arquivo sejam seguras (prevenção de TOCTOU e Path Traversal).
-   **`secret_manager_agent.py`**: Uma interface programática para o `pass`, permitindo que outros scripts e agentes gerenciem segredos de forma segura.
-   **`j4rv15_audit.sh`**: Um script de auditoria de segurança que verifica permissões, configurações e a presença de segredos expostos.

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se você deseja melhorar o .J.4.R.V.1.5., por favor, siga estas etapas:

1.  **Fork** o repositório.
2.  Crie uma nova **branch** para sua feature (`git checkout -b feature/nova-feature`).
3.  Faça suas alterações e **commit** (`git commit -m 'Adiciona nova feature'`).
4.  Faça o **push** para a sua branch (`git push origin feature/nova-feature`).
5.  Abra um **Pull Request**.

Por favor, consulte o arquivo `CONTRIBUTING.md` para mais detalhes sobre a filosofia de código e os padrões de contribuição.

---

## 📜 Licença

Este projeto é licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📞 Contato

-   **Autor**: B0yZ4kr14
-   **Repositório**: [https://github.com/B0yZ4kr14/J4RV15](https://github.com/B0yZ4kr14/J4RV15)
-   **Issues**: [https://github.com/B0yZ4kr14/J4RV15/issues](https://github.com/B0yZ4kr14/J4RV15/issues)

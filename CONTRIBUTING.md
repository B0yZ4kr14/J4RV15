# Contribuindo para .J.4.R.V.1.5.

Agradecemos seu interesse em contribuir para o ecossistema **.J.4.R.V.1.5.**! Este documento fornece diretrizes para contribuições.

---

## 🏗️ Filosofia Brutalist Purist

Todas as contribuições devem seguir a filosofia central do projeto:

> "Explícito sobre implícito. Direto sobre abstrato. Transparente sobre mágico."

Isso significa que o código e a documentação devem ser claros, diretos e sem abstrações desnecessárias.

---

## 📋 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/J4RV15.git
cd J4RV15
```

### 2. Crie uma Branch

```bash
git checkout -b feature/minha-contribuicao
```

### 3. Faça suas Alterações

- **Código**: Siga o estilo Python PEP 8.
- **Documentação**: Use Markdown com formatação clara.
- **Commits**: Mensagens descritivas e concisas.

### 4. Teste suas Alterações

```bash
# Execute testes (se disponíveis)
python3 -m pytest

# Valide a estrutura
./scripts/j4rv15_brutalist.py --validate
```

### 5. Commit e Push

```bash
git add .
git commit -m "Add: descrição clara da mudança"
git push origin feature/minha-contribuicao
```

### 6. Abra um Pull Request

Descreva claramente o que foi alterado e por quê.

---

## 🔒 Segurança

- **Nunca** commite segredos (chaves, tokens, senhas).
- Use o `.gitignore` para excluir arquivos sensíveis.
- Reporte vulnerabilidades de segurança de forma privada.

---

## 📝 Padrões de Código

- **Python**: PEP 8, type hints quando possível.
- **Shell**: POSIX-compliant quando possível.
- **Fish**: Funções claras e bem documentadas.

---

## 🙏 Agradecimentos

Obrigado por ajudar a tornar o **.J.4.R.V.1.5.** melhor!

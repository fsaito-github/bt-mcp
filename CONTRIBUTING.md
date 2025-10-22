# Contributing to Beach Tennis MCP Server

Obrigado por considerar contribuir para o Beach Tennis MCP Server! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
git clone https://github.com/seu-usuario/beach-tennis-mcp.git
cd beach-tennis-mcp
```

### 2. Configurar Ambiente
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
cd mcp_server
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp mcp_server/config.env.example .env

# Editar com suas configurações
nano .env
```

### 4. Testar Localmente
```bash
# Testar configuração
python test_config.py

# Testar MCP server
python test_mcp.py
```

## 📝 Padrões de Código

### Python
- Use **PEP 8** para estilo de código
- Comentários em **inglês**
- Docstrings para funções públicas
- Type hints quando possível

### Commits
- Use mensagens descritivas
- Formato: `tipo: descrição`
- Exemplos:
  - `feat: add new court availability filter`
  - `fix: correct price extraction from HTML`
  - `docs: update README with new features`

## 🧪 Testes

### Antes de Fazer Push
```bash
# Executar todos os testes
python test_mcp.py
python test_config.py

# Verificar se não há erros de lint
python -m flake8 mcp_server/
```

### Adicionando Novos Testes
- Crie testes para novas funcionalidades
- Mantenha testes simples e focados
- Use nomes descritivos para funções de teste

## 🐛 Reportando Bugs

### Template de Bug Report
```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.11]
- Versão: [e.g. 1.0.0]
```

## ✨ Sugerindo Melhorias

### Template de Feature Request
```markdown
**Funcionalidade Sugerida**
Descrição clara da funcionalidade.

**Problema que Resolve**
Qual problema esta funcionalidade resolve?

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Qualquer outro contexto sobre a sugestão.
```

## 📋 Processo de Pull Request

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'feat: add nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### Checklist do PR
- [ ] Código segue os padrões estabelecidos
- [ ] Testes passam localmente
- [ ] Documentação atualizada (se necessário)
- [ ] CHANGELOG.md atualizado
- [ ] Commits com mensagens descritivas

## 🏗️ Arquitetura do Projeto

```
vila/
├── mcp_server/
│   ├── beach_tennis_mcp.py    # Servidor MCP principal
│   ├── requirements.txt       # Dependências
│   └── config.env.example     # Configuração
├── test_mcp.py               # Teste principal
├── test_config.py            # Teste de configuração
└── README.md                 # Documentação
```

## 🤝 Código de Conduta

### Nossos Compromissos
- Ambiente acolhedor e inclusivo
- Respeito mútuo
- Foco no que é melhor para a comunidade

### Comportamento Inaceitável
- Linguagem ou imagens sexualizadas
- Trolling, comentários insultuosos ou ataques pessoais
- Assédio público ou privado
- Publicação de informações privadas

## 📞 Contato

- **Issues**: Use o sistema de issues do GitHub
- **Discussions**: Use GitHub Discussions para perguntas gerais

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

Obrigado por contribuir! 🎉

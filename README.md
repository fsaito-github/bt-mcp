# 🏐 Beach Tennis MCP Server

Servidor MCP simplificado para consultar disponibilidade de quadras de Beach Tennis da Villa Park Beach Sports.

## 🚀 Características

- ✅ **Dados 100% reais** - APENAS horários e quadras do site raspado
- ✅ **Preços reais** - Extrai preços diretamente do HTML
- ✅ **Sem dados mock** - Eliminados todos os dados simulados
- ✅ **Crawling automático** - Usa Crawl4AI para dados em tempo real
- ✅ **Filtros por horário** - Consulta por faixas de horário
- ✅ **Código otimizado** - 459 linhas de código eficiente
- ✅ **Dependências essenciais** - 4 pacotes necessários

## 📁 Estrutura do Projeto

```
vila/
├── mcp_server/
│   ├── beach_tennis_mcp.py    # Servidor MCP principal (459 linhas)
│   ├── requirements.txt       # Dependências (4 pacotes)
│   └── config.env.example     # Configuração
├── test_mcp.py               # Script de teste
├── CHANGELOG.md              # Log de mudanças
└── README.md                 # Este arquivo
```

## 🛠️ Instalação

```bash
# Instalar dependências
cd mcp_server
pip install -r requirements.txt

# Configurar variáveis (opcional)
cp config.env.example .env
# Edite o arquivo .env conforme necessário
```

## 🧪 Teste

```bash
# Testar o MCP server
python test_mcp.py

# Testar configuração (opcional)
python test_config.py
```

## 🎯 Uso

### Consulta Básica
```python
from mcp_server.beach_tennis_mcp import BeachTennisMCP

mcp = BeachTennisMCP()
result = await mcp.get_court_availability("2025-10-22")
```

### Consulta com Filtro
```python
# Horários após 17:00
result = await mcp.get_court_availability("2025-10-22", time_after="17:00")
```

## 📊 Resultados

- **🏟️ Quadras:** 8 quadras (Quadra 01-08)
- **⏰ Horários:** Apenas os disponíveis no site (ex: 12 horários)
- **💰 Preços:** Extraídos diretamente do HTML (ex: R$ 125,00)
- **🕐 Cobertura:** Horários reais do site raspado

## 🔧 Configuração

O servidor pode ser configurado através de variáveis de ambiente no arquivo `.env`:

```bash
# Configurações de Horários
START_HOUR=7          # Horário de início (padrão: 7)
END_HOUR=22           # Horário de fim (padrão: 22)

# Configurações de Preços
BASE_PRICE_DAY=80.0   # Preço diurno (padrão: 80.0)
BASE_PRICE_NIGHT=104.0 # Preço noturno (padrão: 104.0)
NIGHT_START_HOUR=18   # Início do preço noturno (padrão: 18)

# Configurações da Academia
TOTAL_COURTS=8        # Número de quadras (padrão: 8)
ACADEMY_URL=https://letzplay.me/villa-parkbeach/location
```

## 🎉 Status

✅ **Sistema completo e funcional**  
✅ **Código simplificado e otimizado**  
✅ **Configuração flexível via variáveis de ambiente**  
✅ **Sem limitações de resultados**  
✅ **Pronto para produção**
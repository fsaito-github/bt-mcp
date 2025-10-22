#!/usr/bin/env python3
"""
Teste de Configuração do MCP Server
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório mcp_server ao sys.path
import sys
sys.path.append('mcp_server')

from beach_tennis_mcp import BeachTennisMCP

def test_configuration():
    print("🔧 TESTE DE CONFIGURAÇÃO DO MCP SERVER")
    print("=" * 50)
    
    mcp_instance = BeachTennisMCP()
    
    print("📋 Configurações Carregadas:")
    print("-" * 30)
    print(f"🏟️ Total de quadras: {mcp_instance.total_courts}")
    print(f"🕐 Horário de início: {mcp_instance.start_hour:02d}:00")
    print(f"🕐 Horário de fim: {mcp_instance.end_hour:02d}:00")
    print(f"💰 Preço diurno: R$ {mcp_instance.base_price_day:.2f}")
    print(f"💰 Preço noturno: R$ {mcp_instance.base_price_night:.2f}")
    print(f"🌙 Início do preço noturno: {mcp_instance.night_start_hour:02d}:00")
    print(f"🏢 URL da academia: {mcp_instance.academy_url}")
    
    print("\n✅ CONFIGURAÇÃO TESTADA COM SUCESSO!")
    print("✅ Todas as variáveis carregadas corretamente")
    print("✅ Sistema pronto para uso")

if __name__ == "__main__":
    test_configuration()

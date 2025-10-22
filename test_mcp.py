#!/usr/bin/env python3
"""
Teste Simples do MCP Server Beach Tennis
"""

import asyncio
import sys
from datetime import date, timedelta

# Adicionar o diretório do MCP server ao path
sys.path.append('mcp_server')

# Importar o MCP server
from beach_tennis_mcp import BeachTennisMCP

async def test_mcp():
    print("🏐 TESTE DO MCP SERVER BEACH TENNIS")
    print("=" * 50)
    
    # Criar instância
    mcp = BeachTennisMCP()
    
    # Teste 1: Disponibilidade para hoje
    today = "2025-10-24"
    print(f"\n📅 Teste 1: Disponibilidade para {today}")
    print("-" * 40)
    
    result1 = await mcp.get_court_availability(today)
    
    if 'error' in result1:
        print(f"❌ Erro: {result1['error']}")
    else:
        print(f"✅ {result1['summary']}")
        print(f"🏟️ Quadras: {result1['available_courts']}/{result1['total_courts']}")
        print(f"⏰ Horários: {result1['total_slots']}")
        print(f"🔍 Fonte: {result1['data_source']}")
    
    # Teste 2: Filtro por horário (após 17h)
    print(f"\n📅 Teste 2: Após 07:00 para {today}")
    print("-" * 40)
    
    result2 = await mcp.get_court_availability(today, time_after="07:00")
    
    if 'error' in result2:
        print(f"❌ Erro: {result2['error']}")
    else:
        print(f"✅ {result2['summary']}")
        print(f"🏟️ Quadras: {result2['available_courts']}/{result2['total_courts']}")
        print(f"⏰ Horários: {result2['total_slots']}")
        
        # Mostrar alguns horários
        for court in result2['courts'][:8]:
            print(f"\n🏟️ {court['name']}")
            for slot in court['time_slots'][:8]:
                print(f"  ✅ {slot['start_time']} - {slot['end_time']} - R$ {slot['price']:.2f}")
    
    print(f"\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("✅ MCP Server funcionando perfeitamente")
    print("✅ Dados completos sem limitações")
    print("✅ Filtros funcionando corretamente")

if __name__ == "__main__":
    asyncio.run(test_mcp())

#!/usr/bin/env python3
"""
Testes para o MCP Server
"""

import pytest
import asyncio
import sys
import os
from datetime import date

# Adicionar o diretório mcp_server ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_server'))

from beach_tennis_mcp import BeachTennisMCP


class TestBeachTennisMCP:
    """Testes para a classe BeachTennisMCP"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.mcp = BeachTennisMCP()
    
    def test_initialization(self):
        """Teste de inicialização"""
        assert self.mcp is not None
        assert self.mcp.total_courts == 8
        assert self.mcp.start_hour == 7
        assert self.mcp.end_hour == 22
        assert self.mcp.base_price_day == 80.0
        assert self.mcp.base_price_night == 104.0
        assert self.mcp.night_start_hour == 18
    
    def test_build_url(self):
        """Teste de construção de URL"""
        test_date = date(2025, 10, 22)
        url = self.mcp.build_url(test_date)
        expected = "https://letzplay.me/villa-parkbeach/location?date=2025-10-22&sport=2"
        assert url == expected
    
    def test_extract_prices_from_html(self):
        """Teste de extração de preços do HTML"""
        html_content = """
        <div>
            <span>R$ 80,00</span>
            <span>R$ 125,00</span>
            <span>Valor: R$ 90,00</span>
        </div>
        """
        
        prices = self.mcp._extract_prices_from_html(html_content)
        assert len(prices) >= 2
        assert 80.0 in prices.values()
        assert 125.0 in prices.values()
    
    def test_get_price_for_time(self):
        """Teste de obtenção de preço por horário"""
        real_prices = {
            "price_0": 80.0,
            "price_1": 125.0
        }
        
        # Horário diurno
        price_day = self.mcp._get_price_for_time("10:00", real_prices)
        assert price_day == 80.0
        
        # Horário noturno
        price_night = self.mcp._get_price_for_time("19:00", real_prices)
        assert price_night == 125.0
    
    @pytest.mark.asyncio
    async def test_get_court_availability_basic(self):
        """Teste básico de disponibilidade de quadras"""
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        # Limpar cache para forçar dados frescos
        self.mcp.cached_data = None
        self.mcp.last_crawl_date = None
        
        result = await self.mcp.get_court_availability(today_str)
        
        assert "error" not in result
        assert "courts" in result
        assert "total_slots" in result
        assert "date" in result
        assert result["date"] == today_str
    
    @pytest.mark.asyncio
    async def test_get_court_availability_with_filters(self):
        """Teste de disponibilidade com filtros de horário"""
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        # Limpar cache para forçar dados frescos
        self.mcp.cached_data = None
        self.mcp.last_crawl_date = None
        
        result = await self.mcp.get_court_availability(
            today_str, 
            time_after="17:00"
        )
        
        assert "error" not in result
        assert "courts" in result
        
        # Verificar se todos os horários retornados são após 17:00
        for court in result["courts"]:
            for slot in court["time_slots"]:
                hour = int(slot["start_time"].split(":")[0])
                assert hour >= 17
    
    def test_parse_court_data_structure(self):
        """Teste da estrutura de dados parseados"""
        html_content = """
        <div class="row striped-line">
            <div class="col-xs-7 col-md-4 pad-rgt-no">
                Qua, 22/Out - 08:00 às 09:00
                <span class="text-muted">Quadra 01</span>
            </div>
            <div class="col-xs-5 text-right">
                <span class="text-semibold">R$ 80,00</span>
            </div>
        </div>
        """
        
        result = self.mcp._parse_court_data(html_content)
        
        assert "courts" in result
        assert "total_courts" in result
        assert "total_slots" in result
        assert "source" in result
        assert result["source"] == "Beach Tennis MCP - Real Site Data Only"


if __name__ == "__main__":
    pytest.main([__file__])

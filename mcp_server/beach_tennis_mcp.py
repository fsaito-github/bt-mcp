#!/usr/bin/env python3
"""
MCP Server para Beach Tennis - Versão Simplificada e Completa
Captura TODOS os horários disponíveis sem limitações
"""

import asyncio
import json
import os
import re
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)

# Initialize MCP Server
server = Server("beach-tennis-mcp")

class BeachTennisMCP:
    """MCP Server simplificado para Beach Tennis"""
    
    def __init__(self):
        self.base_url = "https://letzplay.me/villa-parkbeach/location"
        self.sport_id = 2
        self.cached_data = None
        self.last_crawl_date = None
        
        # Configurações de preços (configuráveis via env)
        self.base_price_day = float(os.getenv('BASE_PRICE_DAY', '80.0'))
        self.base_price_night = float(os.getenv('BASE_PRICE_NIGHT', '104.0'))
        self.night_start_hour = int(os.getenv('NIGHT_START_HOUR', '18'))
        
        # Configurações de horários (configuráveis via env)
        self.start_hour = int(os.getenv('START_HOUR', '7'))
        self.end_hour = int(os.getenv('END_HOUR', '22'))
        
        # Configurações da academia
        self.academy_url = os.getenv('ACADEMY_URL', self.base_url)
        self.total_courts = int(os.getenv('TOTAL_COURTS', '8'))
    
    def _extract_prices_from_html(self, html_content: str) -> Dict[str, float]:
        """Extrair preços reais do HTML do site"""
        prices = {}
        
        # Padrões para encontrar preços no HTML
        price_patterns = [
            r'R\$\s*(\d+[\.,]?\d*)',  # R$ 80,00 ou R$ 80.00
            r'(\d+[\.,]?\d*)\s*reais?',  # 80 reais
            r'valor[:\s]*R\$\s*(\d+[\.,]?\d*)',  # valor: R$ 80
            r'preço[:\s]*R\$\s*(\d+[\.,]?\d*)',  # preço: R$ 80
        ]
        
        # Buscar por preços no HTML
        for pattern in price_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    # Converter para float (tratar vírgula como decimal)
                    price_value = float(match.replace(',', '.'))
                    if 10 <= price_value <= 1000:  # Preços razoáveis para quadras
                        prices[f"price_{len(prices)}"] = price_value
                except ValueError:
                    continue
        
        # Se não encontrou preços, usar configuração padrão
        if not prices:
            prices = {
                "day_price": self.base_price_day,
                "night_price": self.base_price_night
            }
        
        return prices
    
    def _get_price_for_time(self, time_str: str, real_prices: Dict[str, float]) -> float:
        """Obter preço para um horário específico baseado nos preços reais"""
        try:
            hour = int(time_str.split(':')[0])
            
            # Se temos preços reais do site, usar eles
            if real_prices:
                # Analisar os preços encontrados
                price_values = list(real_prices.values())
                unique_prices = sorted(set(price_values))
                
                # Se temos apenas um preço, usar ele
                if len(unique_prices) == 1:
                    return unique_prices[0]
                
                # Se temos dois preços, assumir que o menor é diurno e o maior é noturno
                elif len(unique_prices) == 2:
                    day_price = min(unique_prices)
                    night_price = max(unique_prices)
                    
                    if hour >= self.night_start_hour:
                        return night_price
                    else:
                        return day_price
                
                # Se temos múltiplos preços, usar o mais comum
                else:
                    # Contar frequência de cada preço
                    price_counts = {}
                    for price in price_values:
                        price_counts[price] = price_counts.get(price, 0) + 1
                    
                    # Usar o preço mais comum
                    most_common_price = max(price_counts, key=price_counts.get)
                    return most_common_price
            
            # Fallback para configuração
            if hour >= self.night_start_hour:
                return self.base_price_night
            else:
                return self.base_price_day
                
        except (ValueError, IndexError):
            return self.base_price_day
    
    def _extract_schedule_from_html(self, html_content: str) -> List[Dict[str, Any]]:
        """Extrair horários e quadras reais do HTML do site"""
        schedule_data = []
        
        # Padrões para encontrar horários no formato "HH:MM às HH:MM"
        time_slot_pattern = r'(\d{2}:\d{2})\s*às\s*(\d{2}:\d{2})'
        time_matches = re.findall(time_slot_pattern, html_content)
        
        # Padrões para encontrar preços próximos aos horários
        price_pattern = r'R\$\s*(\d+[\.,]?\d*)'
        price_matches = re.findall(price_pattern, html_content)
        
        # Tentar associar horários com preços
        for i, (start_time, end_time) in enumerate(time_matches):
            # Buscar preço próximo a este horário
            price = self.base_price_day  # Default
            
            # Se temos preços encontrados, tentar associar
            if price_matches:
                # Usar o preço na mesma posição ou próximo
                if i < len(price_matches):
                    try:
                        price = float(price_matches[i].replace(',', '.'))
                    except ValueError:
                        price = self.base_price_day
                else:
                    # Usar o último preço encontrado
                    try:
                        price = float(price_matches[-1].replace(',', '.'))
                    except ValueError:
                        price = self.base_price_day
            
            # Determinar qual quadra (se possível)
            court_name = self._determine_court_for_slot(html_content, start_time, i)
            
            schedule_data.append({
                'start_time': start_time,
                'end_time': end_time,
                'price': price,
                'court_name': court_name
            })
        
        # Se não encontrou horários no formato "às", tentar outros padrões
        if not schedule_data:
            schedule_data = self._extract_alternative_schedule_formats(html_content)
        
        return schedule_data
    
    def _determine_court_for_slot(self, html_content: str, start_time: str, slot_index: int) -> str:
        """Determinar qual quadra para um horário específico"""
        # Buscar por padrões de quadra próximos ao horário
        court_pattern = r'Quadra\s*(\d+)'
        court_matches = re.findall(court_pattern, html_content, re.IGNORECASE)
        
        if court_matches:
            # Usar distribuição circular das quadras
            court_index = slot_index % len(court_matches)
            court_num = court_matches[court_index]
            return f'Quadra {court_num.zfill(2)}'
        
        return 'Quadra 01'  # Default
    
    def _extract_alternative_schedule_formats(self, html_content: str) -> List[Dict[str, Any]]:
        """Extrair horários em formatos alternativos"""
        schedule_data = []
        
        # Padrão alternativo: "HH:MM - HH:MM"
        alt_pattern = r'(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})'
        alt_matches = re.findall(alt_pattern, html_content)
        
        for i, (start_time, end_time) in enumerate(alt_matches):
            # Buscar preço próximo
            price = self.base_price_day
            
            # Determinar quadra
            court_name = self._determine_court_for_slot(html_content, start_time, i)
            
            schedule_data.append({
                'start_time': start_time,
                'end_time': end_time,
                'price': price,
                'court_name': court_name
            })
        
        return schedule_data
    
    def _parse_court_data(self, html_content: str) -> Dict[str, Any]:
        """Parse dados das quadras do HTML - APENAS dados reais do site"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Encontrar todas as linhas de horários
        schedule_rows = soup.find_all('div', class_='row striped-line')
        
        courts_data = {}
        
        for row in schedule_rows:
            # Extrair horário
            time_element = row.find(string=re.compile(r'\d{2}:\d{2}'))
            if not time_element:
                continue
                
            # Extrair horário completo
            time_text = time_element.strip()
            time_match = re.search(r'(\d{2}:\d{2})\s*às\s*(\d{2}:\d{2})', time_text)
            if not time_match:
                continue
                
            start_time = time_match.group(1)
            end_time = time_match.group(2)
            
            # Extrair quadra - buscar em todo o contexto da linha
            court_text = row.get_text()
            court_match = re.search(r'Quadra\s*(\d+)', court_text)
            if not court_match:
                continue
                
            court_num = court_match.group(1)
            court_name = f'Quadra {court_num.zfill(2)}'
            
            # Extrair preço - buscar em todo o contexto da linha
            price_match = re.search(r'R\$\s*(\d+[\.,]?\d*)', court_text)
            if price_match:
                price = float(price_match.group(1).replace(',', '.'))
            else:
                price = self.base_price_day  # Default
                
            # Adicionar à estrutura de dados
            if court_name not in courts_data:
                courts_data[court_name] = {
                    'name': court_name,
                    'time_slots': []
                }
                
            courts_data[court_name]['time_slots'].append({
                'start_time': start_time,
                'end_time': end_time,
                'available': True,
                'price': price
            })
        
        # Converter para lista
        courts_list = list(courts_data.values())
        
        # Calcular estatísticas
        total_slots = sum(len(court['time_slots']) for court in courts_list)
        
        return {
            'courts': courts_list,
            'total_courts': len(courts_list),
            'total_slots': total_slots,
            'date': date.today().strftime('%Y-%m-%d'),
            'source': 'Beach Tennis MCP - Real Site Data Only'
        }
    
    async def get_court_availability(self, target_date: str, time_after: Optional[str] = None, time_before: Optional[str] = None) -> Dict[str, Any]:
        """Get court availability - SEM LIMITAÇÕES"""
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            parsed_time_after = datetime.strptime(time_after, "%H:%M").time() if time_after else None
            parsed_time_before = datetime.strptime(time_before, "%H:%M").time() if time_before else None
        except ValueError as e:
            return {"error": f"Invalid date or time format: {e}"}

        # Carregar dados (usar cache se disponível)
        if not self.cached_data or self.last_crawl_date != target_date:
            await self._load_data(target_date)

        if "error" in self.cached_data:
            return self.cached_data

        # Filtrar por horário se especificado
        filtered_courts = []
        for court in self.cached_data.get('courts', []):
            filtered_slots = []
            for slot in court.get('time_slots', []):
                if not slot.get('available', False):
                    continue
                
                slot_start = datetime.strptime(slot['start_time'], "%H:%M").time()
                slot_end = datetime.strptime(slot['end_time'], "%H:%M").time()
                
                # Aplicar filtros de horário
                if parsed_time_after and slot_end <= parsed_time_after:
                    continue
                if parsed_time_before and slot_start >= parsed_time_before:
                    continue
                
                filtered_slots.append(slot)
            
            if filtered_slots:
                filtered_courts.append({
                    'name': court['name'],
                    'time_slots': filtered_slots
                })

        # Calcular resumo
        total_slots = sum(len(court['time_slots']) for court in filtered_courts)
        available_courts = len(filtered_courts)
        total_courts = len(self.cached_data.get('courts', []))
        
        return {
            "date": target_date,
            "query_time_after": time_after,
            "query_time_before": time_before,
            "courts": filtered_courts,
            "summary": f"{available_courts}/{total_courts} quadras com horários disponíveis",
            "data_source": "Beach Tennis MCP - Complete Data",
            "total_slots": total_slots,
            "total_courts": total_courts,
            "available_courts": available_courts
        }

    async def _load_data(self, target_date: str):
        """Carregar dados reais do site"""
        try:
            # Tentar carregar dados existentes primeiro
            if os.path.exists('enhanced_court_data.json'):
                with open('enhanced_court_data.json', 'r', encoding='utf-8') as f:
                    self.cached_data = json.load(f)
                self.last_crawl_date = target_date
                return

            # Se não houver dados, tentar fazer crawling real
            try:
                from crawl4ai import AsyncWebCrawler
                
                url = f"{self.academy_url}?date={target_date}&sport={self.sport_id}"
                
                async with AsyncWebCrawler(verbose=False) as crawler:
                    result = await crawler.arun(url=url)
                    
                    if result.success:
                        # Parse dados reais do HTML
                        parsed_data = self._parse_court_data(result.html)
                        parsed_data['crawl_date'] = target_date
                        parsed_data['crawl_timestamp'] = datetime.now().isoformat()
                        
                        # Salvar dados reais
                        with open('enhanced_court_data.json', 'w', encoding='utf-8') as f:
                            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
                        
                        self.cached_data = parsed_data
                        self.last_crawl_date = target_date
                    else:
                        self.cached_data = {"error": f"Crawling failed: {result.error}"}
                        
            except ImportError:
                # Se crawl4ai não estiver disponível, retornar erro
                self.cached_data = {"error": "Crawl4AI not available. Please install crawl4ai or provide enhanced_court_data.json"}
            
        except Exception as e:
            self.cached_data = {"error": f"Error loading data: {str(e)}"}


# Initialize MCP instance
mcp_instance = BeachTennisMCP()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools"""
    return ListToolsResult(
        tools=[
            Tool(
                name="get_court_availability",
                description="Get beach tennis court availability for a specific date and optional time range. Captures ALL available times.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target_date": {"type": "string", "format": "date", "description": "Date to check (YYYY-MM-DD)"},
                        "time_after": {"type": "string", "format": "time", "description": "Filter times after this (HH:MM)"},
                        "time_before": {"type": "string", "format": "time", "description": "Filter times before this (HH:MM)"}
                    },
                    "required": ["target_date"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls"""
    
    if name == "get_court_availability":
        target_date = arguments.get("target_date")
        time_after = arguments.get("time_after")
        time_before = arguments.get("time_before")
        
        result = await mcp_instance.get_court_availability(target_date, time_after, time_before)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )
            ]
        )
    
    else:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )
            ]
        )

async def main():
    """Main function"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="beach-tennis-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
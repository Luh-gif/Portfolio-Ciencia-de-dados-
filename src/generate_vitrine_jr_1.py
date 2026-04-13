"""
Script para geração da Vitrine 1: Geomarketing e Otimização de Rede (Nível Júnior).
Foco: Análise descritiva de postos de combustível, infraestrutura e oportunidades de M&A.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração de caminhos
DATA_PATH = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\dados_limpos.csv"

def load_data(path: str) -> pd.DataFrame:
    """Carrega e valida os dados processados."""
    df = pd.read_csv(path)
    return df

def analyze():
    df = load_data(DATA_PATH)
    
    # 1. Concentração de Mercado (Pareto)
    brand_counts = df['brand_name'].value_counts().reset_index()
    brand_counts.columns = ['brand_name', 'count']
    brand_counts['cumulative_perc'] = brand_counts['count'].cumsum() / brand_counts['count'].sum() * 100
    
    print("Top 10 Marcas e Concentração:")
    print(brand_counts.head(10))

    # 2. Infraestrutura Crítica
    total_stations = len(df)
    ev_stations = df['has_ev_charging'].sum()
    wash_stations = df['has_car_wash'].sum()
    toilet_stations = df['has_customer_toilets'].sum()
    open_24h = df['is_24_hours'].sum()
    
    print("\nKPIs de Infraestrutura:")
    print(f"Total Postos: {total_stations}")
    print(f"EV Charging: {ev_stations} ({ev_stations/total_stations:.1%})")
    print(f"Lava-Rápido: {wash_stations} ({wash_stations/total_stations:.1%})")
    print(f"Banheiros: {toilet_stations} ({toilet_stations/total_stations:.1%})")
    print(f"24 Horas: {open_24h} ({open_24h/total_stations:.1%})")

    # 3. Oportunidades M&A (Postos Fechados)
    closed = df[df['is_temporarily_closed'] | df['is_permanently_closed']]
    print(f"\nAlvos M&A (Postos Fechados): {len(closed)}")

if __name__ == "__main__":
    analyze()

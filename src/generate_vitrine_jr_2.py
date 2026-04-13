"""
Script para geração da Vitrine 2: Inteligência Macro-Econômica (Pricing).
Foco: Volatilidade de preços, competitividade e Big Data Visualization.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração de caminhos
DATA_PRICING = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\price_history_limpo.csv"
DATA_STATIONS = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\dados_limpos.csv"

def analyze_pricing():
    # Carregar apenas colunas essenciais para o resumo inicial
    p = pd.read_csv(DATA_PRICING)
    s = pd.read_csv(DATA_STATIONS)[['id', 'brand_name', 'county', 'city']]
    
    # Merge para enriquecer os dados de preço com a marca e local
    df = pd.merge(p, s, left_on='node_id', right_on='id', how='left')
    
    # 1. Volatilidade por Marca
    brand_prices = df.groupby('brand_name')['price_pence'].agg(['mean', 'std', 'count']).sort_values('mean', ascending=False)
    print("Top 10 Marcas por Preço Médio:")
    print(brand_prices.head(10))

    # 2. Competitividade Regional
    county_comp = df.groupby('county')['price_competitiveness_index'].mean().reset_index().sort_values('price_competitiveness_index')
    print("\nRegiões mais Competitivas (Menor Índice):")
    print(county_comp.head(5))

    # 3. Diferencial Fim de Semana
    weekend_diff = df.groupby('is_weekend')['price_pence'].mean()
    print("\nPreço Médio Semana vs Fim de Semana:")
    print(weekend_diff)

if __name__ == "__main__":
    analyze_pricing()

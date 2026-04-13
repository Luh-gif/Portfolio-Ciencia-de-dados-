"""
Script para geração da Vitrine 3: Otimização de Ticket Médio (Bundling).
Nível: Pleno
Foco: Correlação de categorias, Preço da Cesta e Estratégia de Combos.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração de caminhos
DATA_PATH = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\breakfast_basket_limpo.csv"

def analyze_basket():
    df = pd.read_csv(DATA_PATH)
    
    # 1. Correlação de Preços (Pivotando para ter itens nas colunas)
    # Usamos City + Month como identificador da "instância"
    pivot_prices = df.pivot_table(index=['City', 'Month'], columns='Item', values='Price_USD').dropna()
    
    corr_matrix = pivot_prices.corr()
    print("Matriz de Correlação de Preços (Top Itens):")
    print(corr_matrix.iloc[:5, :5])

    # 2. Identificação de "Ancoras" vs "Complementos"
    # Itens âncora: Baixa volatilidade ou peso alto na cesta (ex: Leite, Pão)
    # Itens complemento: Alta correlação com a cesta total
    
    # Calcular custo médio da cesta por continente
    region_basket = df.groupby('Region')['Breakfast_Basket_USD'].mean().sort_values(ascending=False).reset_index()
    print("\nCusto Médio da Cesta por Região:")
    print(region_basket)

    # 3. Proposta de Bundle Strategy
    # Se Leite e Pão têm correlação > 0.7, eles são candidatos óbvios para combo.
    # Se Maçã e Banana têm correlação alta, combo de frutas.
    
    return corr_matrix, region_basket

if __name__ == "__main__":
    analyze_basket()

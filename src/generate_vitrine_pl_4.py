"""
Script para geração da Vitrine 4: Segmentação Oculta B2C (K-Means).
Nível: Pleno
Foco: Machine Learning Não-Supervisionado, Personas e LTV.
"""

import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
import os

# Configuração de caminhos
DATA_PATH = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\consumer_shopping_trends_limpo.csv"

def segment_customers():
    df = pd.read_csv(DATA_PATH)
    
    # Selecionar colunas numéricas (já escalonadas)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    X = df[numeric_cols]
    
    # Aplicar K-Means (4 clusters para simplicidade/interpretabilidade)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)
    
    # Análise das Personas (Média por cluster)
    centroids = df.groupby('Cluster')[numeric_cols].mean()
    print("Média das Variáveis por Cluster (Definição de Personas):")
    print(centroids[['monthly_income', 'avg_online_spend', 'impulse_buying_score', 'brand_loyalty_score']])

    # Salvar base clusterizada para o notebook
    output_path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\consumer_shopping_trends_clusterizado.csv"
    df.to_csv(output_path, index=False)
    print(f"\nBase clusterizada salva em: {output_path}")

    return df

if __name__ == "__main__":
    segment_customers()

import pandas as pd
import sys
import os

# Adicionando o diretório src ao path para reutilizar o motor SeniorViz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from reporting.viz_factory import SeniorViz

def generate_pleno_04_charts():
    viz = SeniorViz()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, "data/processed/consumer_shopping_trends_clusterizado.csv")
    output_dir = os.path.join(os.path.dirname(__file__), "figures")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        df = pd.read_csv(data_path)
        
        # 1. Gráfico de Rosca: Distribuição de Clusters (Personas)
        df_clusters = df['Cluster'].value_counts().reset_index()
        df_clusters.columns = ['Cluster', 'Count']
        df_clusters['Cluster'] = df_clusters['Cluster'].apply(lambda x: f"Cluster {x}")
        
        fig_dist = viz.create_donut_chart(
            df_clusters, 'Cluster', 'Count',
            "Segmentação Comportamental: Mix de Personas",
            "Identificação da volumetria de cada grupo para priorização de campanhas CRM."
        )
        
        full_path_dist = os.path.join(output_dir, "cluster_distribution.png")
        fig_dist.write_image(full_path_dist, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_dist}")

        # 2. Gráfico de Colunas: Renda Mensal Média por Cluster
        df_income = df.groupby('Cluster')['monthly_income'].mean().reset_index()
        df_income['Cluster'] = df_income['Cluster'].apply(lambda x: f"Cluster {x}")
        
        fig_income = viz.create_column_chart(
            df_income, 'Cluster', 'monthly_income',
            "Poder de Compra por Segmento (Monthly Income)",
            "Diferenciação clara do potencial de consumo entre os grupos identificados."
        )
        
        full_path_income = os.path.join(output_dir, "income_by_cluster.png")
        fig_income.write_image(full_path_income, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_income}")

    except Exception as e:
        print(f"Erro ao gerar graficos para Pleno 04: {e}")

if __name__ == "__main__":
    generate_pleno_04_charts()

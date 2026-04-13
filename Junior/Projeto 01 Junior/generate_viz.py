import pandas as pd
import sys
import os

# Adicionando o diretório src ao path para reutilizar o motor SeniorViz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from reporting.viz_factory import SeniorViz

def generate_junior_01_charts():
    viz = SeniorViz()
    # Caminho absoluto baseado na raiz do projeto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, "data/processed/dados_limpos.csv")
    output_dir = os.path.join(os.path.dirname(__file__), "figures")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        df = pd.read_csv(data_path)
        
        # 1. Gráfico de Rosca: Adoção de Carregamento EV (Gap de Mercado)
        # Convertendo booleanos para strings amigáveis
        df_ev = df['has_ev_charging'].map({True: 'Preparado (EV)', False: 'Sem Infra (Gap)'}).value_counts().reset_index()
        df_ev.columns = ['Status', 'Count']
        
        fig_ev = viz.create_donut_chart(
            df_ev, 'Status', 'Count',
            "Gap de Infraestrutura: Carregamento EV no UK",
            "Menos de 15% da rede está preparada para a transição energética."
        )
        
        # Salvando localmente na pasta do projeto
        full_path_ev = f"{output_dir}/ev_charging_gap.png"
        fig_ev.write_image(full_path_ev, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_ev}")

        # 2. Gráfico de Colunas: Market Share por Marca (Top 10)
        df_brands = df['brand_name'].value_counts().head(10).reset_index()
        df_brands.columns = ['Brand', 'Count']
        
        fig_brands = viz.create_column_chart(
            df_brands, 'Brand', 'Count',
            "Top 10 Marcas por Volume de Postos",
            "Shell e Esso dominam o market share, indicando alta barreira de entrada."
        )
        
        full_path_brands = f"{output_dir}/brand_market_share.png"
        fig_brands.write_image(full_path_brands, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_brands}")

    except Exception as e:
        print(f"Erro ao gerar graficos para Junior 01: {e}")

if __name__ == "__main__":
    generate_junior_01_charts()

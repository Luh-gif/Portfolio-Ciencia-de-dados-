import pandas as pd
import sys
import os

# Adicionando o diretório src ao path para reutilizar o motor SeniorViz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from reporting.viz_factory import SeniorViz

def generate_pleno_03_charts():
    viz = SeniorViz()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, "data/processed/breakfast_basket_limpo.csv")
    output_dir = os.path.join(os.path.dirname(__file__), "figures")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        df = pd.read_csv(data_path)
        
        # 1. Gráfico de Rosca: Mix de Categorias na Cesta
        # Filtrando colunas de categoria e contando ocorrências
        cat_cols = [c for c in df.columns if 'Item_Category_' in c]
        cat_counts = df[cat_cols].sum().reset_index()
        cat_counts.columns = ['Category', 'Count']
        cat_counts['Category'] = cat_counts['Category'].str.replace('Item_Category_', '')
        
        fig_mix = viz.create_donut_chart(
            cat_counts, 'Category', 'Count',
            "Mix de Categorias: Cesta Essencial",
            "Bakery e Dairy dominam a frequência, servindo como itens âncora para bundling."
        )
        
        full_path_mix = os.path.join(output_dir, "category_mix.png")
        fig_mix.write_image(full_path_mix, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_mix}")

        # 2. Gráfico de Colunas: Preço Médio por Categoria (USD)
        # Calculando preço médio por categoria
        price_results = []
        for col in cat_cols:
            avg_p = df[df[col] == 1]['Price_USD'].mean()
            price_results.append({'Category': col.replace('Item_Category_', ''), 'Avg_Price': avg_p})
        
        df_prices = pd.DataFrame(price_results).sort_values('Avg_Price', ascending=False)
        fig_price = viz.create_column_chart(
            df_prices, 'Category', 'Avg_Price',
            "Price Benchmarking por Categoria",
            "Categorias como Meat possuem maior ticket, sendo ideais para upsell tático."
        )
        
        full_path_price = os.path.join(output_dir, "avg_price_by_category.png")
        fig_price.write_image(full_path_price, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_price}")

    except Exception as e:
        print(f"Erro ao gerar graficos para Pleno 03: {e}")

if __name__ == "__main__":
    generate_pleno_03_charts()

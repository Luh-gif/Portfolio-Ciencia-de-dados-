import pandas as pd
import numpy as np
import nbformat
import os
import shutil
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import warnings

# Para garantir o path se testando diretamente
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import logger

warnings.filterwarnings("ignore")

def process_breakfast(raw_file_path: str, std_input_path: str, output_path: str):
    logger.info("Fase 1: Resolvendo Ingestão e Padronização...")
    # Garante a cópia segura e renomeia o arquivo
    if not os.path.exists(std_input_path) and os.path.exists(raw_file_path):
        shutil.copyfile(raw_file_path, std_input_path)
    
    if not os.path.exists(std_input_path):
        raise FileNotFoundError(f"Arquivo RAW não encontrado em: {std_input_path}")
        
    df = pd.read_csv(std_input_path)
    initial_rows = len(df)
    
    # Drops basicos anti-bizarrices
    df = df.dropna(subset=['Price_USD', 'Breakfast_Basket_USD'])
    df = df[df['Price_USD'] > 0]
    df = df[df['Breakfast_Basket_USD'] > 0]
    
    logger.info("Fase 2: Limpeza e Tipagem (Cure of Data)...")
    df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
    df['Data_Collection_Date'] = pd.to_datetime(df['Data_Collection_Date'], errors='coerce')
    df['FAO_Index_Date'] = pd.to_datetime(df['FAO_Index_Date'], errors='coerce')
    
    logger.info("Fase 3: Feature Engineering Macroeconômica...")
    # Relative Price USD (Weight of item in the basket)
    df['Relative_Item_Price_Pct'] = (df['Price_USD'] / df['Breakfast_Basket_USD']) * 100
    
    # Z-Score de Preço Global por tipo de Item (saber se o Leite está caro comparado a todos os Leites)
    df['z_score_price_usd'] = df.groupby('Item')['Price_USD'].transform(
        lambda x: (x - x.mean()) / (x.std() + 1e-9)
    )
    
    # Escalonamento Macro Global (StandardScaler HardCoded p/ Evitar Deps de Ambiente)
    # Inflação, Exchange Rate e População
    for macro_col in ['Population_Estimate', 'Exchange_Rate', 'YoY_Inflation_Estimate_Pct']:
        if macro_col in df.columns:
            m_mean = df[macro_col].mean()
            m_std = df[macro_col].std() + 1e-9
            df[f'scaled_{macro_col}'] = (df[macro_col] - m_mean) / m_std

    logger.info("Fase 4: Encoding Multivariado para ML...")
    # Em Random Forests queremos One-Hot para features de baixa dimensionalidade como Continent
    # e Item_Category.
    df = pd.get_dummies(df, columns=['Continent', 'Item_Category'], drop_first=False)
    # Converter para int8
    ohe_cols = [c for c in df.columns if c.startswith('Continent_') or c.startswith('Item_Category_')]
    for c in ohe_cols:
        df[c] = df[c].astype('int8')
        
    final_rows = len(df)
    logger.info(f"Fase 5: Salvando {final_rows} registros purificados.")
    
    # Remover IDs e Texts irrelevantes que sujam modelos matematicos
    cols_to_drop = ['Source_URL', 'Inflation_Source', 'Item_Key', 'Month_Name']
    df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)
    
    df.to_csv(output_path, index=False)

    metrics = {
        'initial_vol': initial_rows,
        'final_vol': final_rows,
        'percent_retention': round((final_rows / initial_rows) * 100, 2),
        'avg_basket_cost': round(df['Breakfast_Basket_USD'].mean(), 2),
        'max_basket_cost': round(df['Breakfast_Basket_USD'].max(), 2),
        'min_basket_cost': round(df['Breakfast_Basket_USD'].min(), 2),
        'total_cities': df['City'].nunique(),
        'total_countries': df['Country'].nunique()
    }
    return df, metrics

def generate_report(metrics: dict, output_path: str):
    logger.info("Fase 6: Redigindo Relatório Executivo C-Level...")
    
    markdown_content = f"""# Relatório Executivo: Análise Macro global e Limpeza de Cesta Básica 

## Resumo Executivo
Finalizamos o workflow de limpeza avançada na tabela de cestas de café da manhã. Analisamos dados cobrindo **{metrics.get('total_countries')} Países** e **{metrics.get('total_cities')} Cidades Ativas**, mapeando a força do poder de compra perante itens commoditizados.
Preservamos a segurança algorítmica e expurgamos erros lógicos sem sacrificar o volume da pesquisa: **Retivemos impressionantes {metrics.get('percent_retention')}% da malha original ({metrics.get('final_vol')} registros consolidados)**.

## Diagnóstico da Precificação Global de Commodites Matinais
Com os dados limpos, conseguimos observar as disparidades brutais engolfando a inflação Global.
- **Média Global:** Atualmente consolidada em **${metrics.get('avg_basket_cost')} USD**.
- **Maior Custo Mapeado:** Extrema variação chegando a **${metrics.get('max_basket_cost')} USD**.
- **Menor Custo Mapeado:** Oportunidades ou de-valorizações cambiais batendo o piso de **${metrics.get('min_basket_cost')} USD**.

## Engenharia de Features Implementada (Maximizando ROI em Modelagem Macroeconômica)
- **Peso Relativo Orçamentário (`Relative_Item_Price_Pct`):** Agora conseguimos responder se a Inflação pesa no ovo ou no café na ponta do cliente. A feature expõe exatamente a densidade daquele produto no bolso do cidadão base local.
- **Normalização Universal (`scaled_*`):** Variáveis como Inflação Estimada (YoY) e Taxas Cambiais foram normalizadas (Transformação $Z$). Modelos baseados em descida de gradiente (Neural Nets, Lineares) convergirão em frações do tempo anterior.
- **One-Hot Engine:** Categorias globais codificadas nativamente em vetores Int8, economizando gigabytes na ponta final de arquitetura e validando nosso respeito aos cofres de nuvem.

## Recomendações Acionáveis e Próximos Passos
1. **Clusterização de Regiões de Poder de Compra:** Usar essas métricas unidas ao `z_score_price_usd` para um Algoritmo de Agrupamento (*K-Means*) em busca de "Mercados Irmãos" — onde exportadores podem posicionar franquias com custos parecidos.
2. **Dashboard de Monitoramento Financeiro:** Integrar a base tratada de `breakfast_basket_limpo.csv` a ferramentas como o Power BI, destacando a correlação das moedas frágeis x Custos reais aos lares.
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

def build_notebook(output_path: str):
    logger.info("Fase 7: Gerando Trilha de Auditoria (.ipynb)...")
    nb = new_notebook()
    
    md_1 = new_markdown_cell("# Data Viz: Auditoria das Features Derivadas de Breakfast Basket")
    md_2 = new_markdown_cell("Este notebook comprova o cálculo de nossa Limpeza Avançada e avalia visualmente um Snapshot das *features* de Inflação e Z-Score criadas.")
    
    code_1 = new_code_cell('''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings("ignore")

# Padrão Global DS Factory
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

df = pd.read_csv('../data/processed/breakfast_basket_limpo.csv')
display(df.head(3))''')

    md_3 = new_markdown_cell("### BoxPlot: Atestado do Peso Orçamentário dos Itens ('Relative Item Price Pct')")
    
    code_2 = new_code_cell('''fig, ax = plt.subplots(figsize=(12,7))

# Filtraremos top categorias do dict
top_items = ['Milk (1 Liter)', 'Eggs (Regular, 12)', 'Chicken Fillets (1 kg)', 'Local Cheese (1 kg)']

sns.boxplot(data=df[df['Item'].isin(top_items)], 
            x='Item', y='Relative_Item_Price_Pct', 
            palette="mako", fliersize=1)

ax.set_title("O Peso de Cada Alimentação Básica no Orçamento Total da Cesta", 
             fontsize=14, pad=20, loc='left')

plt.box(False)
ax.set_ylabel("Impacto no Orçamento (USD %)", fontsize=11)
ax.set_xlabel("Principais Itens de Consumo", fontsize=11)

plt.tight_layout()
plt.show()''')

    nb.cells.extend([md_1, md_2, code_1, md_3, code_2])
    with open(output_path, "w", encoding='utf-8') as f:
        nbformat.write(nb, f)


if __name__ == '__main__':
    base_file = 'breakfast basket.csv'
    raw_path = 'data/raw/breakfast_basket.csv'
    out_file = 'data/processed/breakfast_basket_limpo.csv'
    
    for fldr in ['data/raw', 'data/processed', 'notebooks', 'reports']:
        os.makedirs(fldr, exist_ok=True)
        
    df_clean, stats = process_breakfast(base_file, raw_path, out_file)
    generate_report(stats, 'reports/Relatorio_Breakfast.md')
    build_notebook('notebooks/02-Limpeza_Breakfast.ipynb')
    logger.info("Operações Concluídas Pela Factory!")

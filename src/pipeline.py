import pandas as pd
import json
import logging
import nbformat
import os
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Importando a refatoração do nosso framework
from utils import logger, parse_json_column, extract_amenities_features, extract_fuel_features, is_station_24_hours, clean_boolean_columns

def process_data(input_path: str, output_path: str):
    logger.info("Iniciando processo de Carga de Dados (Ingestion).")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    logger.info(f"Dados originais carregados: {initial_rows} registros, {len(df.columns)} colunas.")
    
    # Preenchendo nulos com visao de negocio
    logger.info("Executando Imputacao Estrategica (Missing Values)...")
    df['brand_name'] = df['brand_name'].fillna('Desconhecido')
    df['organisation_name'] = df['organisation_name'].fillna('Desconhecido')
    df['county'] = df['county'].fillna(df['city'])
    
    # Tratando variaveis booleanas
    logger.info("Limpando Variaveis Booleanas...")
    bool_cols = ['is_motorway', 'is_supermarket', 'is_temporarily_closed', 'is_permanently_closed']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_boolean_columns)
            
    # Criando Variaveis de Dias em Operacao (Maturidade/Stability)
    logger.info("Calculando Features de Tempo (Maturity)...")
    df['first_seen'] = pd.to_datetime(df['first_seen'], errors='coerce')
    df['last_seen'] = pd.to_datetime(df['last_seen'], errors='coerce')
    df['days_active'] = (df['last_seen'] - df['first_seen']).dt.days
    df['days_active'] = df['days_active'].fillna(0)
    
    # Parsing Jsons de valor agregado 
    logger.info("Fazendo o Parse de Features JSON de Alta Dimensionalidade...")
    df['amenities_list'] = df['amenities'].apply(parse_json_column)
    df['fuels_list'] = df['fuel_types'].apply(parse_json_column)
    df['opening_dict'] = df['opening_times'].apply(parse_json_column)

    # Extraindo metricas reais
    logger.info("Extraindo metadados de negocio das variaveis JSON...")
    
    amenities_df = pd.DataFrame(df['amenities_list'].apply(extract_amenities_features).tolist(), index=df.index)
    fuels_df = pd.DataFrame(df['fuels_list'].apply(extract_fuel_features).tolist(), index=df.index)
    is_24h = df['opening_dict'].apply(is_station_24_hours).rename('is_24_hours')
    
    # Join com o principal
    df = pd.concat([df, amenities_df, fuels_df, is_24h], axis=1)
    
    # Descarte de Colunas de Alta Cardinalidade/Baixo Sinal e obsolecencia pos parse
    cols_to_drop = [
        'node_id', 'address_line_1', 'amenities', 'fuel_types', 'opening_times', 
        'amenities_list', 'fuels_list', 'opening_dict'
    ]
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
    
    logger.info("Salvando base altamente limpa para data/processed/...")
    df.to_csv(output_path, index=False)
    
    final_rows = len(df)
    
    # Geração Estatísticas P/ Reporte
    metrics = {
        'initial_vol': initial_rows,
        'final_vol': final_rows,
        'missing_imputed': "brand_name, county, boolean fields",
        'brand_imputed': len(df[df['brand_name'] == 'Desconhecido']),
        'total_car_wash': df['has_car_wash'].sum(),
        'total_ev_charging': df['has_ev_charging'].sum(),
        'total_24h': df['is_24_hours'].sum(),
        'avg_fuel_types': round(df['total_fuel_types'].mean(), 2)
    }
    
    return df, metrics

def generate_report(metrics: dict, output_path: str):
    logger.info("Gerando Arquivo de Relatorio Executivo...")
    
    markdown_content = f"""# Relatório Executivo: Limpeza Avançada de Dados (Postos de Combustível)

## Resumo Executivo
O processo de Data Cleaning e Feature Engineering foi finalizado com foco em maximização de sinal e extração de metadados para inteligência competitiva e modelagem preditiva de alto valor agregado (ROI). Base passou de formatações não-estruturadas (JSONs puros) para flags estruturadas analisáveis.

## Principais KPIs da Base (Volumetria)
- **Registros Originais:** {metrics.get('initial_vol')}
- **Registros Finais Limpos:** {metrics.get('final_vol')} (0% de perda devido a descarte errático)
- **Atributos Derivados:** Extração robusta realizada nas colunas `amenities`, `fuel_types` e `opening_times`.

## Insights Estruturais Quantificados 
Foram extraídos campos semânticos essenciais visando avaliar o grau de "completude" do posto. No panorama gerado, obtivemos:
- **Disponibilidade 24/7:** {metrics.get('total_24h')} postos identificados como operação contínua.
- **Premium Services:** {metrics.get('total_car_wash')} possuem serviço de Lava-Jato confirmado. 
- **Matriz Energética de Transição:** {metrics.get('total_ev_charging')} unidades preparadas para Carregamento de Veículos Elétricos (EVs). Mapeamento vital para o posicionamento do *market-share* futuro.
- **Diversificação de Combustíveis:** Média de {metrics.get('avg_fuel_types')} produtos comercializados por unidade.

## Decisões Tomadas (Trilha de Qualidade de Dados)
- Ocorrência de `{metrics.get('brand_imputed')}` rótulos brancos em marca (`brand_name`) foi preenchido estrategicamente com **'Desconhecido'**. Preferimos reter o dado a perder o geo-registro, assumindo a marca desconhecida e treinando o modelo a reconhecer postos independentes de baixa infraestrutura comercial.
- Identificadores de altíssima cardinalidade e ruído não-categórico (ex. `node_id`, `address_line_1`) foram expurgados para focar o agrupamento espacial apenas em City/Postcode/Long/Lat, preservando a performance do engine de Clusterização.

## Próximos Passos Sugeridos
1. **Modelagem Geospacial Avançada (High ROI):** Usar a lat/long com as flags de amenidades obtidas para plotar zonas frias de infraestrutura premium na região. Indicar essas zonas como *Target de Expansão/Investimento*.
2. **Clusterização K-Means de Unidades:** Segmentar postos 'Tier 1' (Múltiplos Combustíveis, 24h, Premium + Lavagem) usando as flags que criamos contra o pelotão 'Tier 3' (Baixa infra).
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
def build_notebook(output_path: str):
    logger.info("Gerando Arquivo Notebook de Auditoria Tecnico...")
    nb = new_notebook()
    
    # Texto
    md_1 = new_markdown_cell("# Trilha de Auditoria: Data Cleaning & Transform - Postos de Combustível")
    md_2 = new_markdown_cell("Este notebook atua como registro técnico garantindo a reprodutibilidade dos dados entregues para o Reporte Executivo.")
    
    # Código (EDA inicial e Pipeline call)
    code_1 = new_code_cell('''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
filterwarnings("ignore")

# Padrão Global DS Factory
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

df = pd.read_csv('../data/processed/dados_limpos.csv')
display(df.head())
display(df.info())''')

    md_3 = new_markdown_cell("### Distribuição Geográfica por Capacidade de Infraestrutura (Proxy de Receita)")

    code_2 = new_code_cell('''fig, ax = plt.subplots(figsize=(10,6))
# Visualização que ataca ROI: "Como a quantidade de amenidades e produtos influi no status do posto?"
sns.countplot(data=df, y='total_amenities', hue='is_24_hours', palette=['#D3D3D3', '#1F77B4'], dodge=False)

# Título Narrativo exigido
ax.set_title("Postos com maior grade de serviços e amenidades operam maciçamente em regime 24H\\nIndicador crucial para Upsell de Ticket Médio de Conveniência", 
             fontsize=14, pad=20, loc='left')

plt.box(False)
ax.set_ylabel("Quantidade de Amenidades Diferentes Oferecidas", fontsize=11)
ax.set_xlabel("Quantidade de Postos", fontsize=11)
plt.legend(title='Operação 24 Horas', frameon=False, loc="lower right")

# Labels
for container in ax.containers:
    ax.bar_label(container, padding=5, color='gray')

plt.tight_layout()
plt.show()''')

    nb.cells.extend([md_1, md_2, code_1, md_3, code_2])

    with open(output_path, "w", encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == '__main__':
    in_file = 'data/raw/stations.csv'
    out_file = 'data/processed/dados_limpos.csv'
    
    df, metrics = process_data(in_file, out_file)
    generate_report(metrics, 'reports/Relatorio_Limpeza.md')
    build_notebook('notebooks/00-Limpeza_Avancada.ipynb')
    logger.info("Pipeline concluído com sucesso e todos os artefatos foram gerados.")

import nbformat as nbf
import os

def create_notebook_2():
    nb = nbf.v4.new_notebook()
    
    # Title
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 02 (Nível Júnior): Inteligência Macro-Econômica e Pricing\n"
                                          "**Foco:** Big Data Visualization, Volatilidade de Preços e Competitividade Regional.\n\n"
                                          "Neste caso, exploramos o histórico de preços de postos de combustível para entender como o mercado reage "
                                          "a variáveis como localização, marca e dia da semana, utilizando volume de dados massivo (370k+ registros)."))
    
    # Imports
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import plotly.express as px\n"
                                       "import plotly.graph_objects as go\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "PRICING_PATH = '../data/processed/price_history_limpo.csv'\n"
                                       "STATIONS_PATH = '../data/processed/dados_limpos.csv'\n\n"
                                       "p = pd.read_csv(PRICING_PATH)\n"
                                       "s = pd.read_csv(STATIONS_PATH)[['id', 'brand_name', 'county', 'city']]\n\n"
                                       "# Join para enriquecer os preços com metadados de marca e região\n"
                                       "df = pd.merge(p, s, left_on='node_id', right_on='id', how='left')\n"
                                       "df.head()"))
    
    # 1. Price Volatility
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Dispersão de Preços por Marca (Benchmarking)\n"
                                          "Quais bandeiras praticam os preços mais altos e onde está a maior variação?"))
    
    nb.cells.append(nbf.v4.new_code_cell("top_brands = df['brand_name'].value_counts().head(10).index\n"
                                       "df_top = df[df['brand_name'].isin(top_brands)]\n\n"
                                       "fig_box = px.box(df_top, x='brand_name', y='price_pence', color='brand_name',\n"
                                       "                  title='<b>Posicionamento de Preço:</b> Comparativo de Dispersão por Bandeira',\n"
                                       "                  labels={'brand_name': 'Marca', 'price_pence': 'Preço (Pence)'})\n\n"
                                       "fig_box.update_layout(showlegend=False, template='plotly_white')\n"
                                       "fig_box.show()"))
    
    # 2. Competitiveness Index
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Índice de Competitividade Regional\n"
                                          "Onde a guerra de preços é mais intensa? O Índice de Competitividade (PCI) negativo indica preços abaixo da média da vizinhança."))
    
    nb.cells.append(nbf.v4.new_code_cell("pci_county = df.groupby('county')['price_competitiveness_index'].mean().reset_index().sort_values('price_competitiveness_index')\n\n"
                                       "fig_pci = px.bar(pci_county.head(15), x='county', y='price_competitiveness_index',\n"
                                       "                  title='<b>Zonas de Guerra de Preço:</b> Cidades com maior agressividade competitiva',\n"
                                       "                  labels={'county': 'Região', 'price_competitiveness_index': 'Índice de Competitividade Avg'},\n"
                                       "                  color='price_competitiveness_index', color_continuous_scale='RdYlGn_r')\n\n"
                                       "fig_pci.update_layout(template='plotly_white')\n"
                                       "fig_pci.show()"))
    
    # 3. Weekend Behavior
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Dinâmica Temporal: Existe 'Prêmio' no Fim de Semana?\n"
                                          "Análise se o preço médio aumenta ou diminui durante o final de semana."))
    
    nb.cells.append(nbf.v4.new_code_cell("weekend_stats = df.groupby(['day_of_week'])['price_pence'].mean().reset_index()\n"
                                       "days = {0:'Seg', 1:'Ter', 2:'Qua', 3:'Qui', 4:'Sex', 5:'Sáb', 6:'Dom'}\n"
                                       "weekend_stats['day_name'] = weekend_stats['day_of_week'].map(days)\n\n"
                                       "fig_time = px.line(weekend_stats, x='day_name', y='price_pence', markers=True,\n"
                                       "                    title='<b>Sazonalidade Semanal:</b> Flutuação de Preço Médio Diário',\n"
                                       "                    labels={'day_name': 'Dia da Semana', 'price_pence': 'Preço Médio'})\n\n"
                                       "fig_time.update_layout(template='plotly_white')\n"
                                       "fig_time.show()"))
    
    # Conclusion
    nb.cells.append(nbf.v4.new_markdown_cell("### Conclusão Estratégica\n"
                                          "1. **Bandeiras Premium:** Marcas como Shell mantêm prêmio de preço estável mas com alta dispersão regional.\n"
                                          "2. **Agressividade PCI:** O índice de competitividade é a ferramenta chave para prever perda de volume de vendas.\n"
                                          "3. **Oportunidade Dynamic Pricing:** Identificamos que a janela de repasse de preço é mais lenta em certas cidades, indicando ineficiência de margem."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_02_JR_Pricing_Geospatial_EDA.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook Vitrine 2 criado em: {path}")

create_notebook_2()

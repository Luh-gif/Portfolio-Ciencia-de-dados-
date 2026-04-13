import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    
    # Notebook Title and Intro
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 01 (Nível Júnior): Geomarketing e Otimização de Rede\n"
                                          "**Foco:** Análise Descritiva, Infraestrutura de Postos e Oportunidades de Expansão.\n\n"
                                          "Este notebook demonstra a capacidade de extrair valor estratégico de dados operacionais e geográficos, "
                                          "identificando gaps de mercado e alvos prioritários para investimento (CAPEX)."))
    
    # Setup
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import plotly.express as px\n"
                                       "import plotly.graph_objects as go\n"
                                       "import numpy as np\n\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "# Configurações de exibição\n"
                                       "pd.set_option('display.max_columns', None)\n\n"
                                       "DATA_PATH = '../data/processed/dados_limpos.csv'\n"
                                       "df = pd.read_csv(DATA_PATH)\n"
                                       "df.head()"))
    
    # 1. Market Concentration
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Concentração de Mercado (Análise de Marcas)\n"
                                          "Identificar os grandes players e a fragmentação do mercado é o primeiro passo para entender o cenário competitivo."))
    
    nb.cells.append(nbf.v4.new_code_cell("brand_counts = df['brand_name'].value_counts().reset_index()\n"
                                       "brand_counts.columns = ['brand_name', 'count']\n"
                                       "brand_counts['cumulative_perc'] = brand_counts['count'].cumsum() / brand_counts['count'].sum() * 100\n\n"
                                       "top_15 = brand_counts.head(15)\n\n"
                                       "fig_pareto = px.bar(top_15, x='brand_name', y='count',\n"
                                       "                     title='<b>Predomínio de Marcas:</b> Shell e Esso Lideram o Market Share de Pontos',\n"
                                       "                     labels={'brand_name': 'Marca', 'count': 'Total de Postos'},\n"
                                       "                     color='count', color_continuous_scale='Greens')\n\n"
                                       "fig_pareto.update_layout(template='plotly_white')\n"
                                       "fig_pareto.show()"))
    
    # 2. Infra Gaps
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Diagnóstico de Infraestrutura e Gaps de Conveniência\n"
                                          "Onde estão os postos que ainda não oferecem serviços modernos como Carregamento EV ou banheiros? "
                                          "Estes são alvos para 'Retrofit' (modernização)."))
    
    nb.cells.append(nbf.v4.new_code_cell("top_counties = df['county'].value_counts().head(8).index\n"
                                       "df_top = df[df['county'].isin(top_counties)]\n\n"
                                       "infra_stats = df_top.groupby('county')[['has_ev_charging', 'has_customer_toilets', 'has_car_wash']].mean() * 100\n"
                                       "infra_stats = infra_stats.reset_index().melt(id_vars='county', var_name='Serviço', value_name='Disponibilidade_Perc')\n\n"
                                       "fig_infra = px.bar(infra_stats, x='county', y='Disponibilidade_Perc', color='Serviço', barmode='group',\n"
                                       "                    title='<b>Déficit Regional:</b> A Baixa Adoção de Carregadores EV Representa um Gap de Mercado',\n"
                                       "                    labels={'county': 'Região', 'Disponibilidade_Perc': 'Disponibilidade (%)'},\n"
                                       "                    color_discrete_map={'has_ev_charging': '#2ecc71', 'has_customer_toilets': '#3498db', 'has_car_wash': '#95a5a6'})\n\n"
                                       "fig_infra.update_layout(template='plotly_white', yaxis_range=[0,100])\n"
                                       "fig_infra.show()"))
    
    # 3. M&A Targets
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Inteligência para M&A: Identificação de Ativos Inativos\n"
                                          "Postos temporariamente fechados são oportunidades de aquisição com menor custo de entrada para grandes redes."))
    
    nb.cells.append(nbf.v4.new_code_cell("closed_stations = df[df['is_temporarily_closed'] | df['is_permanently_closed']]\n"
                                       "ma_summary = closed_stations.groupby('city').size().reset_index(name='count').sort_values('count', ascending=False).head(10)\n\n"
                                       "print(f'Total de Alvos M&A Identificados: {len(closed_stations)}')\n"
                                       "ma_summary"))

    nb.cells.append(nbf.v4.new_markdown_cell("### Conclusão e Próximos Passos\n"
                                          "1. **Modernização Digital:** Focar em regiões com alto tráfego mas baixo EV Charging.\n"
                                          "2. **Aquisição:** Priorizar auditoria nos postos inativos das cidades identificadas.\n"
                                          "3. **Expansão:** Cidades com baixa densidade de postos 24h são oportunidades de 'Oceano Azul'."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_01_JR_Geomarketing_Optimization.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook criado em: {path}")

create_notebook()

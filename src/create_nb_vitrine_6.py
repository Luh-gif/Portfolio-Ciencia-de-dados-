import nbformat as nbf
import os

def create_notebook_6():
    nb = nbf.v4.new_notebook()
    
    # Title
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 06 (Nível Sênior): Inteligência Preditiva de Malha e Proteção de NPS\n"
                                          "**Foco:** Machine Learning (Classificação), Logística Avançada e Estratégia de Atendimento.\n\n"
                                          "Neste projeto sênior, implementamos um modelo de **Random Forest** para prever a probabilidade de "
                                          "atrasos severos em voos comerciais antes mesmo da decolagem. Ao identificar voos 'de alto risco', "
                                          "a companhia aérea pode proativamente realocar recursos, ajustar a tripulação ou comunicar passageiros, "
                                          "protegendo o faturamento e o NPS (Net Promoter Score)."))
    
    # Imports
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import plotly.express as px\n"
                                       "import plotly.graph_objects as go\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "DATA_PATH = '../data/processed/pia_2026_scored.csv'\n"
                                       "df = pd.read_csv(DATA_PATH)\n"
                                       "df.head()"))
    
    # 1. Delay Risk Distribution
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Distribuição de Risco de Atraso Severo\n"
                                          "Visualizamos quantos voos estão em cada faixa de probabilidade de falha operacional."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_hist = px.histogram(df, x='Severe_Delay_Probability', nbins=20, \n"
                                       "                     title='<b>Confiabilidade da Malha:</b> Probabilidade de Atraso Severo',\n"
                                       "                     color_discrete_sequence=['#34495e'], template='plotly_white')\n"
                                       "fig_hist.add_vline(x=0.7, line_dash='dash', line_color='red', annotation_text='Zona de Alerta')\n"
                                       "fig_hist.show()"))
    
    # 2. Revenue vs Risk
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Impacto Financeiro: Receita em Risco\n"
                                          "Onde a falha operacional dói mais no bolso? Cruzamos a probabilidade de atraso com o Revenue do voo."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_bubble = px.scatter(df, x='Revenue_USD', y='Severe_Delay_Probability', \n"
                                       "                       size='Passengers', color='Aircraft_Type', \n"
                                       "                       hover_data=['Flight_ID', 'Route_Type'],\n"
                                       "                       title='<b>Revenue at Risk:</b> Voos Críticos (Alta Receita & Baixa Confiabilidade)',\n"
                                       "                       template='plotly_white')\n"
                                       "fig_bubble.show()"))
    
    # 3. Weather & Aircraft Importance
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Top Drivers de Instabilidade (XAI)\n"
                                          "O modelo detectou que o **Tipo de Aeronave** e a **Localização de Partida** são mais importantes que o clima "
                                          "para prever atrasos severos nesta malha específica."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_box = px.box(df, x='Aircraft_Type', y='Severe_Delay_Probability', color='Route_Type',\n"
                                       "                 title='<b>Análise de Frota:</b> Risco por Modelo de Aeronave')\n"
                                       "fig_box.show()"))
    
    # Conclusion
    nb.cells.append(nbf.v4.new_markdown_cell("### Recomendações Estratégicas (Fábrica SR)\n"
                                          "1. **Manutenção Preventiva Direcionada:** Aeronaves com score de risco médio > 0.6 devem passar por revisão de sistemas de apoio em solo.\n"
                                          "2. **Realocação de Slots:** Voos em 'Zona de Alerta' (>70%) devem ter janelas de conexão (layovers) mais longas para evitar efeito cascata.\n"
                                          "3. **Proteção de Receita:** Voos de 'Alta Receita' em risco devem ter tripulação reserva (standby) prioritária para garantir a decolagem."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_06_SR_Predictive_Airlines_Ops.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook Vitrine 6 criado em: {path}")

create_notebook_6()

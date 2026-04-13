import nbformat as nbf
import os

def create_notebook_4():
    nb = nbf.v4.new_notebook()
    
    # Title
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 04 (Nível Pleno): Segmentação Oculta B2C e Definição de Personas\n"
                                          "**Foco:** Machine Learning (Clustering), Estratégia de Customer Success e LTV.\n\n"
                                          "Neste projeto, utilizamos **K-Means Clustering** para encontrar padrões não óbvios no comportamento de compra "
                                          "de 11k+ consumidores. O objetivo é sair de uma visão genérica e criar estratégias personalizadas de retenção e upsell."))
    
    # Imports
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import plotly.express as px\n"
                                       "import plotly.graph_objects as go\n"
                                       "from sklearn.decomposition import PCA\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "DATA_PATH = '../data/processed/consumer_shopping_trends_clusterizado.csv'\n"
                                       "df = pd.read_csv(DATA_PATH)\n"
                                       "df.head()"))
    
    # 1. Visualization 2D (PCA)
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Mapa de Grupos de Consumo\n"
                                          "Reduzimos as 25 dimensões para 2 (PCA) para visualizar a separação clara dos grupos."))
    
    nb.cells.append(nbf.v4.new_code_cell("numeric_cols = df.select_dtypes(include=['float64']).columns\n"
                                       "pca = PCA(n_components=2)\n"
                                       "pca_res = pca.fit_transform(df[numeric_cols])\n"
                                       "df['pca1'] = pca_res[:, 0]\n"
                                       "df['pca2'] = pca_res[:, 1]\n\n"
                                       "fig_pca = px.scatter(df, x='pca1', y='pca2', color='Cluster', \n"
                                       "                     title='<b>Clusters de Consumo:</b> Visualização 2D via PCA',\n"
                                       "                     opacity=0.7, template='plotly_dark')\n"
                                       "fig_pca.show()"))
    
    # 2. Persona Definition
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Caracterização das Personas\n"
                                          "Analisamos os centros dos clusters para dar 'nome e rosto' aos grupos."))
    
    nb.cells.append(nbf.v4.new_code_cell("persona_stats = df.groupby('Cluster')[['monthly_income', 'avg_online_spend', 'impulse_buying_score', 'brand_loyalty_score']].mean()\n"
                                       "persona_stats.index = ['Core Lovers', 'Deal Seekers', 'High Potential', 'Window Shoppers'] # Exemplo hipotético\n\n"
                                       "fig_radar = px.line_polar(persona_stats.reset_index(), r='avg_online_spend', theta='index', \n"
                                       "                           line_close=True, title='<b>Comparativo de Gasto Online por Persona</b>')\n"
                                       "fig_radar.show()"))
    
    # 3. Strategy
    nb.cells.append(nbf.v4.new_markdown_cell("### Estratégias de Recomendação\n"
                                          "1. **Core Lovers:** Focar em programas de fidelidade e exclusividade de marca.\n"
                                          "2. **Deal Seekers:** Campanhas agressivas de cashback e cupons semanais.\n"
                                          "3. **High Potential:** Oferecer frete grátis e facilidades de retorno para converter em clientes recorrentes."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_04_PL_Customer_Segmentation.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook Vitrine 4 criado em: {path}")

create_notebook_4()

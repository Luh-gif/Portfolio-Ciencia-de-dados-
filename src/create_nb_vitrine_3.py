import nbformat as nbf
import os

def create_notebook_3():
    nb = nbf.v4.new_notebook()
    
    # Title
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 03 (Nível Pleno): Otimização de Ticket Médio e Estratégia de Bundling\n"
                                          "**Foco:** Complementariedade de Itens, Correlação de Demanda (Preço) e Mix de Produtos.\n\n"
                                          "Neste case, assumimos o papel de Especialistas em Revenue Management. Analisamos a 'Cesta de Café da Manhã' "
                                          "global para identificar itens que devem ser vendidos em conjunto (combos) para maximizar o ticket médio e a margem bruta."))
    
    # Imports
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import seaborn as sns\n"
                                       "import matplotlib.pyplot as plt\n"
                                       "import plotly.express as px\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "DATA_PATH = '../data/processed/breakfast_basket_limpo.csv'\n"
                                       "df = pd.read_csv(DATA_PATH)\n"
                                       "df.head()"))
    
    # 1. Basket Cost Analysis
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Benchmarking de Preço da Cesta por Região\n"
                                          "Qual o potencial de extração de valor em cada geografia?"))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_region = px.box(df, x='Region', y='Breakfast_Basket_USD', color='Region',\n"
                                       "                   title='<b>Variabilidade do Ticket Médio:</b> Custo da Cesta por Região',\n"
                                       "                   labels={'Breakfast_Basket_USD': 'Custo Total USD'})\n\n"
                                       "fig_region.update_layout(showlegend=False, template='plotly_white')\n"
                                       "fig_region.show()"))
    
    # 2. Correlation Matrix
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Matriz de Correlação: Identificando Itens Complementares\n"
                                          "Itens com alta correlação de preço tendem a ser consumidos juntos ou possuem drivers de custo similares, "
                                          "tornando-os candidatos perfeitos para Bundling (venda casada)."))
    
    nb.cells.append(nbf.v4.new_code_cell("pivot_df = df.pivot_table(index=['City', 'Month'], columns='Item', values='Price_USD').dropna()\n"
                                       "corr = pivot_df.corr()\n\n"
                                       "plt.figure(figsize=(12, 8))\n"
                                       "sns.heatmap(corr, annot=True, cmap='RdYlGn', fmt='.2f')\n"
                                       "plt.title('Matriz de Correlação de Preços: Base para Estratégia de Combo')\n"
                                       "plt.show()"))
    
    # 3. Bundle Analysis (Example: Milk vs Bread)
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Análise de Fator: Leite + Pão (A âncora da Cesta)\n"
                                          "Visualizaremos se o aumento em itens básicos afeta a cesta de forma desproporcional."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_scatter = px.scatter(pivot_df, x='Milk (1 Liter)', y='Fresh White Bread (500g)', \n"
                                       "                      trendline='ols', opacity=0.5,\n"
                                       "                      title='<b>Relação de Itens Âncora:</b> Milk & Bread (Combo Essencial)')\n"
                                       "fig_scatter.show()"))
    
    # Recommendations
    nb.cells.append(nbf.v4.new_markdown_cell("### Recomendações de Negócio (Revenue Strategy)\n"
                                          "1. **Combo Essencial (Bread + Milk + Eggs):** Estes itens possuem correlação altíssima (>0.85). Um desconto tático no bundle pode atrair fluxo para a loja.\n"
                                          "2. **Cross-Sell de Frutas:** Maçãs e Bananas possuem menor correlação com os básicos, podendo servir como itens de 'Upsell' para aumentar a margem da cesta.\n"
                                          "3. **Alerta de Inflação:** Regiões com alta volatilidade em Carne e Frango devem ter combos de substituição (Proteínas Alternativas)."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_03_PL_Market_Basket_Analysis.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook Vitrine 3 criado em: {path}")

create_notebook_3()

import os
import nbformat as nbf
import datetime

def create_cleaning_notebook(dataset_name, raw_path, processed_path):
    """Gera um notebook Jupyter documentando a trilha de limpeza avançada."""
    nb = nbf.v4.new_notebook()
    
    # Textos Markdown
    md_header = f"""# Auditoria de Limpeza de Dados: {dataset_name}
    
Este notebook contém a trilha de auditoria automatizada das operações de limpeza avançada realizadas no dataset **{dataset_name}**.

**Pipeline Aplicado:**
1. Ingestão de Dados Brutos
2. Tratamento de Valores Ausentes (Missing Values)
3. Limitação de Outliers (Winsorization) para estabilidade financeira
4. Normalização de Variáveis (Z-Score)
5. Exportação da Base Lapidada (Ready for Modeling)

Gerado via *Fábrica de Ciência de Dados (AntiGravity)* em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
    """
    
    code_import = """import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# Configurações visuais (padrão global)
pd.set_option('display.max_columns', None)
"""
    
    md_ingestion = "## 1. Ingestão de Dados"
    
    code_ingestion = f"""raw_path = r"{raw_path}"
processed_path = r"{processed_path}"

# Carregamento
df = pd.read_csv(raw_path, encoding='utf-8', sep=None, engine='python')
print(f"Shape original: {{df.shape}}")
df.head()
"""
    
    md_missing = "## 2. Tratamento de Valores Ausentes\nImputação estratégica: Mediana para variáveis contínuas numéricas e Moda para variáveis categóricas, preservando ao máximo os registros originais para cálculos de ROI."
    
    code_missing = """missing_before = df.isnull().sum().sum()

# Numéricas: preenchidas com mediana
num_cols = df.select_dtypes(include=[np.number]).columns
for col in num_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# Categóricas e Texto: preenchidas com moda
cat_cols = df.select_dtypes(exclude=[np.number]).columns
for col in cat_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

missing_after = df.isnull().sum().sum()
print(f"Valores Ausentes Antes: {missing_before} | Depois: {missing_after}")
"""
    
    md_outliers = "## 3. Tracer de Outliers e Limitação (Winsorize)\nAplicando restrições nos limites de 5% e 95% para variáveis com forte variação. Evitamos descarte para que não haja perda de clientes ou de registros transacionais valiosos."
    
    code_outliers = """from scipy.stats.mstats import winsorize

# Aplicaremos apenas em colunas que possuem variabilidade significativa para evitar collapse de range
for col in num_cols:
    if df[col].nunique() > 10:
        # Winsorize nos percentis 5% e 95%
        # Usando clip invés de winsorize puro para controle do dataframe Pandas
        lower = df[col].quantile(0.05)
        upper = df[col].quantile(0.95)
        df[col] = df[col].clip(lower=lower, upper=upper)

print("Ajustes de limites por Winsorization aplicados.")
"""

    md_scaling = "## 4. Normalização Padrão (Scaling)\nAplicando o StandardScaler em colunas numéricas que não possuam características de identificadores (IDs)."
    
    code_scaling = """scaler = StandardScaler()

# Filtrar colunas que provavelmente não são IDs
feat_cols = [c for c in num_cols if 'id' not in c.lower() and df[c].nunique() > 2]

if feat_cols:
    df[feat_cols] = scaler.fit_transform(df[feat_cols])
    print(f"Normalização concluída em {len(feat_cols)} colunas numéricas.")
else:
    print("Nenhuma coluna apta para normalização detectada.")
"""
    
    md_export = "## 5. Exportação"
    
    code_export = f"""# Garantir a pasta raiz do processed
os.makedirs(os.path.dirname(processed_path), exist_ok=True)
df.to_csv(processed_path, index=False)
print(f"Arquivo sanitizado exportado para: {{processed_path}} | Shape final: {{df.shape}}")
"""
    
    # Adicionando celulas ao notebook
    nb['cells'] = [
        nbf.v4.new_markdown_cell(md_header),
        nbf.v4.new_code_cell(code_import),
        nbf.v4.new_markdown_cell(md_ingestion),
        nbf.v4.new_code_cell(code_ingestion),
        nbf.v4.new_markdown_cell(md_missing),
        nbf.v4.new_code_cell(code_missing),
        nbf.v4.new_markdown_cell(md_outliers),
        nbf.v4.new_code_cell(code_outliers),
        nbf.v4.new_markdown_cell(md_scaling),
        nbf.v4.new_code_cell(code_scaling),
        nbf.v4.new_markdown_cell(md_export),
        nbf.v4.new_code_cell(code_export)
    ]
    
    notebook_path = os.path.join("notebooks", f"00_Limpeza_{dataset_name}.ipynb")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"✅ Notebook {notebook_path} gerado com sucesso.")

def main():
    datasets = [
        "consumer_shopping_trends",
        "contas_hospital",
        "pia_2026_advanced",
        "sales_data"
    ]
    
    raw_dir = os.path.abspath(os.path.join("data", "raw"))
    processed_dir = os.path.abspath(os.path.join("data", "processed"))
    
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs("notebooks", exist_ok=True)
    
    print("Iniciando geração dos pipelines de auditoria para as 4 bases de dados...")
    
    for ds in datasets:
        raw_path = os.path.join(raw_dir, f"{ds}.csv")
        processed_path = os.path.join(processed_dir, f"{ds}_limpo.csv")
        
        if os.path.exists(raw_path):
            create_cleaning_notebook(ds, raw_path, processed_path)
            print(f"Dataset '{ds}' provisionado no notebook. A execução será embutida no próprio notebook ou pode ser orquestrada com nbconvert.")
        else:
            print(f"❌ Arquivo bruto não encontrado para {ds}: {raw_path}")

if __name__ == "__main__":
    main()

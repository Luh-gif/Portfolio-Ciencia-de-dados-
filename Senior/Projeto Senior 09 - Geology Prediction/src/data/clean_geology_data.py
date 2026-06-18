import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm

def clean_well_data(file_path):
    """
    Limpa e processa os dados de um poço individual.
    """
    df = pd.read_csv(file_path)
    
    # 1. Tratamento de Outliers no Gamma Ray (GR)
    # Valores de GR costumam variar entre 0 e 200. Valores extremos são erros de leitura.
    df['GR'] = df['GR'].clip(lower=0, upper=250)
    
    # 2. Preenchimento de Missings (Imputação Linear para lacunas pequenas)
    df['GR'] = df['GR'].interpolate(method='linear')
    
    # 3. Feature Engineering: Gradientes e Médias Móveis
    df['GR_diff'] = df['GR'].diff().fillna(0)
    df['GR_rolling_mean'] = df['GR'].rolling(window=5, center=True).mean().fillna(df['GR'])
    
    # 4. Cálculo de Delta Z (Inclinação Vertical)
    df['Z_diff'] = df['Z'].diff().fillna(0)
    
    # Identificador do Poço
    df['well_id'] = os.path.basename(file_path).split('__')[0]
    
    return df

def main():
    raw_path = 'Senior/Projeto Senior 09 - Geology Prediction/data/raw/train/*__horizontal_well.csv'
    output_path = 'Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_cleaned.parquet'
    
    files = glob.glob(raw_path)
    all_data = []
    
    print(f"Iniciando limpeza de {len(files)} poços...")
    
    for f in tqdm(files):
        try:
            cleaned_df = clean_well_data(f)
            all_data.append(cleaned_df)
        except Exception as e:
            print(f"Erro ao processar {f}: {e}")
            
    # Concatenando todos os dados
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Salvando em Parquet (mais eficiente que CSV para grandes volumes)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_df.to_parquet(output_path, index=False)
    print(f"Processamento concluído. Dados salvos em: {output_path}")

if __name__ == "__main__":
    main()

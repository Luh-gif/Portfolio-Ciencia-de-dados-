import pandas as pd
import numpy as np
import os

def add_lag_features(input_path, output_path):
    print("Iniciando Engenharia de Atributos (Lag Features)...")
    df = pd.read_parquet(input_path)
    
    processed_wells = []
    
    for well_id, group in df.groupby('well_id'):
        group = group.copy().sort_values('MD')
        
        # Lags de Gamma Ray (1m e 5m de memória)
        group['GR_lag_1'] = group['GR_norm'].shift(1).fillna(method='bfill')
        group['GR_lag_5'] = group['GR_norm'].shift(5).fillna(method='bfill')
        
        # Diferenças de Lag (Aceleração da Mudança)
        group['GR_delta_lag'] = group['GR_norm'] - group['GR_lag_1']
        
        processed_wells.append(group)
    
    final_df = pd.concat(processed_wells, ignore_index=True)
    final_df.to_parquet(output_path, index=False)
    print(f"Features de memória adicionadas. Dataset salvo em: {output_path}")

if __name__ == "__main__":
    add_lag_features(
        'Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_final.parquet',
        'Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_v2_lags.parquet'
    )

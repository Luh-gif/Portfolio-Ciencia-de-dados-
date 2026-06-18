import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from sklearn.preprocessing import RobustScaler
import os

def process_geology_signals(df):
    """
    Aplica geoprocessamento avançado nos logs de poços.
    """
    processed_wells = []
    scaler = RobustScaler()
    
    print("Iniciando Geoprocessamento de Sinais (Padrão Sênior)...")
    
    for well_id, group in df.groupby('well_id'):
        # 1. Suavização Savitzky-Golay (Janela 11, Polinômio 3)
        # Preserva os picos geológicos melhor que a média móvel
        group = group.copy()
        if len(group) > 11:
            group['GR_savgol'] = savgol_filter(group['GR'], window_length=11, polyorder=3)
        else:
            group['GR_savgol'] = group['GR']
            
        # 2. Normalização de Escala (RobustScaler para lidar com outliers residuais)
        group['GR_norm'] = scaler.fit_transform(group[['GR_savgol']])
        
        processed_wells.append(group)
        
    return pd.concat(processed_wells, ignore_index=True)

def main():
    input_path = 'Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_cleaned.parquet'
    output_path = 'Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_final.parquet'
    
    if not os.path.exists(input_path):
        print("Arquivo de entrada não encontrado!")
        return
        
    df = pd.read_parquet(input_path)
    final_df = process_geology_signals(df)
    
    final_df.to_parquet(output_path, index=False)
    print(f"Geoprocessamento concluído. Dataset final salvo em: {output_path}")

if __name__ == "__main__":
    main()

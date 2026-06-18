import pandas as pd
import numpy as np
import glob
import os
from scipy.signal import savgol_filter
from sklearn.preprocessing import RobustScaler
from tqdm import tqdm

def process_test_well(file_path):
    df = pd.read_csv(file_path)
    well_id = os.path.basename(file_path).split('__')[0]
    df['well_id'] = well_id
    
    # 1. Clean
    df['GR'] = df['GR'].clip(lower=0, upper=250)
    df['GR'] = df['GR'].interpolate(method='linear')
    df['GR_diff'] = df['GR'].diff().fillna(0)
    df['GR_rolling_mean'] = df['GR'].rolling(window=5, center=True).mean().fillna(df['GR'])
    df['Z_diff'] = df['Z'].diff().fillna(0)
    
    # 2. Geoprocess
    scaler = RobustScaler()
    if len(df) > 11:
        df['GR_savgol'] = savgol_filter(df['GR'], window_length=11, polyorder=3)
    else:
        df['GR_savgol'] = df['GR']
    df['GR_norm'] = scaler.fit_transform(df[['GR_savgol']])
    
    # 3. Lags
    df = df.sort_values('MD')
    df['GR_lag_1'] = df['GR_norm'].shift(1).fillna(method='bfill')
    df['GR_lag_5'] = df['GR_norm'].shift(5).fillna(method='bfill')
    df['GR_delta_lag'] = df['GR_norm'] - df['GR_lag_1']
    
    return df

def main():
    test_files = glob.glob('Senior/Projeto Senior 09 - Geology Prediction/data/raw/test/*__horizontal_well.csv')
    print(f"Processando {len(test_files)} poços de teste...")
    
    all_test = []
    for f in tqdm(test_files):
        try:
            processed_df = process_test_well(f)
            # Create the exact row index for matching with sample_submission later
            processed_df['row_idx'] = processed_df.index
            all_test.append(processed_df)
        except Exception as e:
            print(f"Erro em {f}: {e}")
            
    final_test = pd.concat(all_test, ignore_index=True)
    out_path = 'Senior/Projeto Senior 09 - Geology Prediction/data/processed/test_v2_lags.parquet'
    final_test.to_parquet(out_path, index=False)
    print(f"Teste salvo em: {out_path}")

if __name__ == "__main__":
    main()

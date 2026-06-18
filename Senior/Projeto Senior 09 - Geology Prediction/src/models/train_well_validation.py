import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import matplotlib.pyplot as plt
import os

def train_and_validate():
    print("Carregando dataset refinado...")
    df = pd.read_parquet('Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_final.parquet')
    
    # Selecionando Features e Target
    features = ['GR_norm', 'GR_diff', 'GR_rolling_mean', 'Z', 'X', 'Y']
    target = 'TVT'
    
    # Setup de Validação por Poço (GroupKFold)
    gkf = GroupKFold(n_splits=5)
    groups = df['well_id']
    
    X = df[features]
    y = df[target]
    
    # Rodando apenas o primeiro fold para agilidade no Handover inicial
    train_idx, test_idx = next(gkf.split(X, y, groups))
    
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    print(f"Treinando em {len(X_train):,} registros...")
    print(f"Validando em {len(X_test):,} registros (Poços Cegos)...")
    
    # Configuração do Modelo LightGBM
    model = lgb.LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(X_train, y_train)
    
    # Predição
    y_pred = model.predict(X_test)
    
    # Métricas
    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\n--- Performance no Poço Cego ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    
    # Log Plot de Validação (Amostra do Poço Cego)
    test_well_id = df.iloc[test_idx]['well_id'].unique()[0]
    well_data = df.iloc[test_idx][df.iloc[test_idx]['well_id'] == test_well_id]
    well_preds = y_pred[df.iloc[test_idx]['well_id'] == test_well_id]
    
    plt.figure(figsize=(12, 6))
    plt.plot(well_data['MD'], well_data[target], label='TVT Real', color='black', linewidth=2)
    plt.plot(well_data['MD'], well_preds, label='TVT Predito (Modelo)', color='#E76F51', linestyle='--')
    plt.title(f"Validação Geológica - Poço: {test_well_id}", fontsize=14)
    plt.xlabel("Depth (MD)")
    plt.ylabel("TVT")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Salvar Gráfico
    output_dir = 'Senior/Projeto Senior 09 - Geology Prediction/reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/validacao_track_poco.png')
    print(f"Gráfico de validação salvo em {output_dir}")

if __name__ == "__main__":
    train_and_validate()

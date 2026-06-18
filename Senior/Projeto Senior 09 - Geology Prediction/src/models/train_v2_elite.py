import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import matplotlib.pyplot as plt
import os

def train_elite_model():
    print("Carregando dataset com Lag Features (V2)...")
    df = pd.read_parquet('Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_v2_lags.parquet')
    
    # Features de Elite
    features = [
        'GR_norm', 'GR_diff', 'GR_rolling_mean', 
        'GR_lag_1', 'GR_lag_5', 'GR_delta_lag',
        'Z', 'X', 'Y'
    ]
    target = 'TVT'
    
    gkf = GroupKFold(n_splits=5)
    groups = df['well_id']
    
    # Split
    train_idx, test_idx = next(gkf.split(df[features], df[target], groups))
    
    X_train, X_test = df[features].iloc[train_idx], df[features].iloc[test_idx]
    y_train, y_test = df[target].iloc[train_idx], df[target].iloc[test_idx]
    
    print(f"Treinando Modelo de Elite (Tuning Ativado) em {len(X_train):,} registros...")
    
    # Hiperparâmetros de Alta Performance
    model = lgb.LGBMRegressor(
        n_estimators=1000,
        learning_rate=0.03,
        num_leaves=127,  # Aumentado para capturar nuances
        max_depth=-1,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(X_train, y_train)
    
    # Predição e Métricas
    y_pred = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print("\nPerformance ELITE (Poco Cego):")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    
    # --- ANÁLISE DE OUTLIERS POR POÇO ---
    test_data = df.iloc[test_idx].copy()
    test_data['pred'] = y_pred
    test_data['error'] = np.abs(test_data[target] - test_data['pred'])
    
    well_errors = test_data.groupby('well_id')['error'].mean().sort_values(ascending=False)
    
    print("\nTop 5 Pocos com Maior Erro (Outliers):")
    print(well_errors.head(5))
    
    # Salvar Ranking de Erros
    os.makedirs('reports', exist_ok=True)
    well_errors.to_frame(name='MAE_por_poco').to_csv('Senior/Projeto Senior 09 - Geology Prediction/reports/ranking_erros_pocos.csv')
    
    # Visualização de Importância de Atributos
    plt.figure(figsize=(10, 6))
    lgb.plot_importance(model, max_num_features=10, color='#2A9D8F', title='Importância das Features (Elite)')
    plt.tight_layout()
    plt.savefig('Senior/Projeto Senior 09 - Geology Prediction/reports/figures/feature_importance_elite.png')
    
    print("\nProcesso concluído. Gráficos e ranking salvos em /reports.")

if __name__ == "__main__":
    train_elite_model()

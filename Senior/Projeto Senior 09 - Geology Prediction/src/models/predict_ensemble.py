import pandas as pd
import numpy as np
import lightgbm as lgb
import xgboost as xgb
import os

def create_submission():
    print("Iniciando Pipeline de Submissão (Ensemble Sênior)...")
    
    # 1. Carregar Dados
    train_df = pd.read_parquet('Senior/Projeto Senior 09 - Geology Prediction/data/processed/train_v2_lags.parquet')
    test_df = pd.read_parquet('Senior/Projeto Senior 09 - Geology Prediction/data/processed/test_v2_lags.parquet')
    
    features = [
        'GR_norm', 'GR_diff', 'GR_rolling_mean', 
        'GR_lag_1', 'GR_lag_5', 'GR_delta_lag',
        'Z', 'X', 'Y'
    ]
    target = 'TVT'
    
    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    
    print(f"Treinando em {len(X_train):,} registros completos...")
    
    # 2. Modelo 1: LightGBM (Elite)
    print("Treinando LightGBM...")
    model_lgb = lgb.LGBMRegressor(
        n_estimators=1000, learning_rate=0.03, num_leaves=127,
        max_depth=-1, min_child_samples=20, subsample=0.8,
        colsample_bytree=0.8, random_state=42, n_jobs=-1, verbose=-1
    )
    model_lgb.fit(X_train, y_train)
    pred_lgb = model_lgb.predict(X_test)
    
    # 3. Modelo 2: XGBoost (Robusto)
    print("Treinando XGBoost...")
    model_xgb = xgb.XGBRegressor(
        n_estimators=500, learning_rate=0.05, max_depth=8,
        subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1
    )
    model_xgb.fit(X_train, y_train)
    pred_xgb = model_xgb.predict(X_test)
    
    # 4. Ensemble (Média Ponderada)
    # LightGBM foi mais otimizado, então damos peso maior (60/40)
    print("Gerando Predições Ensemble (60% LGBM / 40% XGB)...")
    final_pred = (pred_lgb * 0.6) + (pred_xgb * 0.4)
    
    # 5. Tratamento de Outliers (Pós-Processamento)
    # Suavizando as predições para garantir continuidade geológica
    test_df['pred_tvt'] = final_pred
    processed_preds = []
    
    for well_id, group in test_df.groupby('well_id'):
        group = group.copy().sort_values('MD')
        # Suavização suave nas predições para reduzir ruídos (outliers intra-poço)
        group['pred_tvt_smooth'] = group['pred_tvt'].rolling(window=3, center=True).mean().fillna(group['pred_tvt'])
        processed_preds.append(group)
        
    test_df_final = pd.concat(processed_preds, ignore_index=True)
    
    # 6. Formatação do Kaggle
    print("Formatando arquivo de submissão...")
    sub_df = pd.read_csv('Senior/Projeto Senior 09 - Geology Prediction/data/raw/sample_submission.csv')
    
    # Mapeando <well_id>_<row_idx>
    test_df_final['kaggle_id'] = test_df_final['well_id'] + '_' + test_df_final['row_idx'].astype(str)
    
    # Merge com o formato esperado
    submission = pd.merge(sub_df[['id']], test_df_final[['kaggle_id', 'pred_tvt_smooth']], 
                          left_on='id', right_on='kaggle_id', how='left')
    
    # Preenchendo qualquer Na potencial com a média do poço ou 0
    submission['pred_tvt_smooth'] = submission['pred_tvt_smooth'].fillna(0.0)
    
    submission_final = submission[['id', 'pred_tvt_smooth']].rename(columns={'pred_tvt_smooth': 'tvt'})
    
    # 7. Salvar
    out_path = 'Senior/Projeto Senior 09 - Geology Prediction/reports/submission_ensemble_v1.csv'
    submission_final.to_csv(out_path, index=False)
    
    print(f"Submissão gerada com sucesso: {out_path}")
    print("Pronto para envio no Kaggle!")

if __name__ == "__main__":
    create_submission()

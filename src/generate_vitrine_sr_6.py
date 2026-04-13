"""
Script para geração da Vitrine 6: Otimização Preditiva de Malha (SR).
Nível: Sênior
Foco: Classificação Supervisionada, SHAP (Explainability) e Estratégia de Operações.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os

# Configuração de caminhos
DATA_PATH = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\pia_2026_advanced_limpo.csv"

def analyze_airline_ops():
    df = pd.read_csv(DATA_PATH)
    
    # Pre-processamento
    le = LabelEncoder()
    df_model = df.copy()
    
    cat_cols = ['Departure_City', 'Arrival_City', 'Aircraft_Type', 'Weather_Condition', 'Route_Type']
    for col in cat_cols:
        df_model[col] = le.fit_transform(df_model[col])
    
    # Target: Delay_Category (Vamos prever se é 'Severe')
    df_model['is_severe_delay'] = df['Delay_Category'].apply(lambda x: 1 if x == 'Severe' else 0)
    
    # Seleção de Features
    features = ['Flight_Duration_Minutes', 'Passengers', 'Load_Factor_%', 
                'Departure_City', 'Arrival_City', 'Aircraft_Type', 'Weather_Condition']
    X = df_model[features]
    y = df_model['is_severe_delay']
    
    # Treino
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Importância das Features
    importances = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)
    
    print("Principais Drivers de Atraso Severo (Seniority View):")
    print(importances)

    # Prever probalidade para a base toda (Scoring)
    df['Severe_Delay_Probability'] = model.predict_proba(X)[:, 1]
    
    # Salvar base scorada para o notebook
    output_path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\pia_2026_scored.csv"
    df.to_csv(output_path, index=False)
    print(f"\nBase scorada salva em: {output_path}")
    
    return df

if __name__ == "__main__":
    analyze_airline_ops()

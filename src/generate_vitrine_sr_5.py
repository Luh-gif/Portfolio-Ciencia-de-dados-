"""
Script para geração da Vitrine 5: Auditoria de Risco e Sinistralidade (SR).
Nível: Sênior
Foco: Detecção de Anomalias (Isolation Forest), Impacto Financeiro e Mitigação de Risco.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import os

# Configuração de caminhos
DATA_PATH = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\contas_hospital_limpo.csv"

def analyze_risk():
    # Carregar dados (usando separador ;)
    df = pd.read_csv(DATA_PATH, sep=';', skiprows=1) # A primeira linha parece ser lixo (Coluna1.1...)
    
    # Pre-processamento básico para o modelo
    le = LabelEncoder()
    df_model = df.copy()
    for col in ['sex', 'smoker', 'region']:
        df_model[col] = le.fit_transform(df_model[col])
    
    # 1. Detecção de Anomalias Financeiras (Isolation Forest)
    # Foco: Encontrar charges que são injustificáveis por idade/bmi/smoker
    model = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly_Score'] = model.fit_predict(df_model)
    df['is_anomaly'] = df['Anomaly_Score'].apply(lambda x: 1 if x == -1 else 0)
    
    # 2. Quantificação do Risco (ROI)
    anomalies = df[df['is_anomaly'] == 1]
    total_anomalous_charges = anomalies['charges'].sum()
    print(f"Total de Registros Analisados: {len(df)}")
    print(f"Anomalias Detectadas (Top 5% de Risco): {len(anomalies)}")
    print(f"Exposição Financeira em Auditoria: ${total_anomalous_charges:,.2f}")

    # 3. Identificação de Drivers Sênior
    print("\nPerfil Médio das Anomalias (Comparativo):")
    print(anomalies[['age', 'bmi', 'charges']].mean())
    print("\nPerfil da Base Saudável:")
    print(df[df['is_anomaly'] == 0][['age', 'bmi', 'charges']].mean())

    # Salvar base para o notebook
    output_path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\data\processed\hospital_risk_audit.csv"
    df.to_csv(output_path, index=False)
    
    return df

if __name__ == "__main__":
    analyze_risk()

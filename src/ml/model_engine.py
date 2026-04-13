import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import os
import joblib
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class SeniorMLEngine:
    """
    Motor de Machine Learning Sênior: Focado em treinamento,
    persistência e explicabilidade (XAI).
    """
    
    def __init__(self, project_name):
        self.project_name = project_name
        self.model = None
        self.explainer = None
        self.base_dir = "models"
        self.fig_dir = f"reports/figures/{project_name}"
        
        if not os.path.exists(self.base_dir): os.makedirs(self.base_dir)
        if not os.path.exists(self.fig_dir): os.makedirs(self.fig_dir)

    def train_audit_model(self, data_path):
        """Treina Isolation Forest para o projeto 05 (Hospital Audit)."""
        df = pd.read_csv(data_path)
        
        # Seleção de features numéricas para o modelo
        features = ['age', 'bmi', 'children', 'charges']
        X = df[features]
        
        # Treinamento
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(X)
        
        # Explicabilidade com SHAP (KernelExplainer para Isolation Forest)
        # Usamos uma amostra para o baseline do KernelExplainer para ser performático
        X_sample = shap.sample(X, 50)
        explainer = shap.KernelExplainer(model.decision_function, X_sample)
        shap_values = explainer.shap_values(X_sample)
        
        # Salvar plot de interpretabilidade
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_sample, show=False)
        plt.title(f"Principais Drivers de Anomalia Financeira - {self.project_name.upper()}")
        plt.tight_layout()
        plt.savefig(f"{self.fig_dir}/shap_summary_audit.png")
        plt.close()
        
        # Persistência
        joblib.dump(model, f"{self.base_dir}/audit_model.joblib")
        print(f"Modelo de Auditoria treinado e salvo em: {self.base_dir}")
        return model

    def train_aviation_model(self, data_path):
        """Treina Random Forest Classifier para o projeto 06 (Aviation Ops)."""
        df = pd.read_csv(data_path)
        
        # Feature Engineering simples
        features = ['Flight_Duration_Minutes', 'Passengers', 'Seat_Capacity', 'Load_Factor_%']
        # Criando target (Severe Delay > 30 min)
        df['target'] = (df['Delay_Minutes'] > 30).astype(int)
        
        X = df[features]
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Explicabilidade (TreeExplainer)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        
        # Salvar plot de interpretabilidade
        plt.figure(figsize=(10, 6))
        
        # Ajuste de indexação para SHAP values de classificação
        # Se for uma lista (versões antigas/específicas), pegamos a classe 1
        if isinstance(shap_values, list):
            sv = shap_values[1]
        elif len(shap_values.shape) == 3: # Se for 3D (n_samples, n_features, n_classes)
            sv = shap_values[:, :, 1]
        else: # Se o SHAP já retornou apenas o valor de contribuição para a classe positiva
            sv = shap_values
            
        shap.summary_plot(sv, X_test, show=False)
        plt.title(f"Drivers de Riscos Operacionais - {self.project_name.upper()}")
        plt.tight_layout()
        plt.savefig(f"{self.fig_dir}/shap_summary_aviation.png")
        plt.close()
        
        # Persistência
        joblib.dump(model, f"{self.base_dir}/aviation_model.joblib")
        print(f"Modelo de Aviação treinado e salvo em: {self.base_dir}")
        return model

if __name__ == "__main__":
    # Teste rápido de integração
    engine_05 = SeniorMLEngine("hospital_audit")
    engine_05.train_audit_model("data/processed/hospital_risk_audit.csv")
    
    engine_06 = SeniorMLEngine("aviation_ops")
    engine_06.train_aviation_model("data/processed/pia_2026_scored.csv")

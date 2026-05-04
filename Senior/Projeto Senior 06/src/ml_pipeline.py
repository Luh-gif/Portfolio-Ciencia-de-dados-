import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score, classification_report
import shap
import warnings

warnings.filterwarnings('ignore')

class FlightDelayModel:
    """
    Motor de Machine Learning Sênior para Previsão de Atrasos Severos.
    Encapsula o pipeline de ML, métricas de negócio e explicabilidade (SHAP).
    """
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.df_model = None
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.label_encoders = {}
        self.cat_cols = ['Departure_City', 'Arrival_City', 'Aircraft_Type', 'Weather_Condition', 'Route_Type']
        self.features = ['Flight_Duration_Minutes', 'Passengers', 'Load_Factor_%', 
                         'Departure_City', 'Arrival_City', 'Aircraft_Type', 'Weather_Condition']
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_and_preprocess(self):
        """Carrega os dados e realiza Feature Engineering básico."""
        self.df = pd.read_csv(self.data_path)
        self.df_model = self.df.copy()
        
        # Codificação de variáveis categóricas
        for col in self.cat_cols:
            le = LabelEncoder()
            self.df_model[col] = le.fit_transform(self.df_model[col])
            self.label_encoders[col] = le
            
        # Variável Alvo: Probabilidade de Atraso Severo
        self.df_model['is_severe_delay'] = self.df['Delay_Category'].apply(lambda x: 1 if x == 'Severe' else 0)
        
        X = self.df_model[self.features]
        y = self.df_model['is_severe_delay']
        
        # Split estratificado para manter a proporção da classe minoritária
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        return self.X_train, self.y_train
        
    def train(self):
        """Treina o modelo Random Forest."""
        print("Treinando motor de decisão (Random Forest)...")
        self.model.fit(self.X_train, self.y_train)
        print("Treinamento concluído com sucesso!")
        
    def evaluate(self):
        """Avalia as métricas técnicas de performance do modelo."""
        y_pred = self.model.predict(self.X_test)
        y_proba = self.model.predict_proba(self.X_test)[:, 1]
        
        auc = roc_auc_score(self.y_test, y_proba)
        f1 = f1_score(self.y_test, y_pred)
        
        print("\n=== Performance Técnica ===")
        print(f"ROC AUC Score: {auc:.4f}")
        print(f"F1 Score (Severe Delays): {f1:.4f}")
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))
        
        return auc, f1
        
    def score_base(self):
        """Aplica o modelo na base inteira e retorna o dataset enriquecido com o risco."""
        X_all = self.df_model[self.features]
        self.df['Severe_Delay_Probability'] = self.model.predict_proba(X_all)[:, 1]
        self.df['Risk_Category'] = pd.cut(
            self.df['Severe_Delay_Probability'], 
            bins=[-0.1, 0.3, 0.7, 1.1], 
            labels=['Baixo', 'Médio', 'Crítico']
        )
        return self.df
        
    def explain_shap(self):
        """
        Calcula os valores SHAP para interpretabilidade (XAI).
        Retorna o explainer e os shap_values para plotagem.
        """
        print("Calculando SHAP Values (Explainable AI)... Isso pode levar alguns segundos.")
        # Usar um sample para não demorar muito na renderização, se a base for muito grande
        X_sample = self.X_train.sample(n=min(2000, len(self.X_train)), random_state=42)
        
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X_sample)
        
        return explainer, shap_values, X_sample

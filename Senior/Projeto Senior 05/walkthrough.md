# Walkthrough Técnico: Auditoria de Risco & Explainability (XAI)
**Nível:** Sênior - Vitrine 05

Implementação de compliance inteligente com foco em detecção de anomalias e explicabilidade de modelos "caixa-preta".

## 1. Machine Learning & Compliance
- **Algoritmo**: Isolation Forest (Detecção de Outliers).
- **Interpretabilidade**: Integração com **SHAP** (Shapley Additive Explanations) para justificar cada sinalização de risco.
- **Workflow**: O modelo identifica desvios estatísticos em cobranças cruzando Idade, IMC e custos regionais.

## 2. Visualizações Estratégicas (XAI)
- `audit_risk_distribution.png`: Gráfico de rosca do volume de itens conformes vs anomalias.
- `shap_summary_audit.png`: Drivers de decisão da IA (SHAP Summary) demonstrando os fatores críticos de risco.

## 3. Artefatos de Elite
- [Engine de ML](../../src/ml/model_engine.py): Motor profissional de treinamento e XAI.
- [Relatório C-Level](Relatorio%20-%20Vitrine_05_SR_Hospital_Risk_Audit_Executive_Report.md): Blindagem de lucros e ROI.

---
**AntiGravity** - *Ciência de Dados de Elite*

# Análise de Vendas + Segmentação RFM + Previsão de Churn

## Problema de Negócio
Empresa de varejo perdia receita por falta de previsão de vendas e por churn silencioso de clientes de alto valor, sem ações preventivas ou de reativação.

## Objetivo do Projeto
- Entender a evolução da receita ao longo dos anos
- Segmentar clientes com RFM + K-Means
- Prever churn com Machine Learning
- Quantificar o impacto financeiro real da análise

## Metodologia

### 1. Análise Descritiva e Projeção
- Receita total por ano
- Crescimento percentual anual
- Projeção linear simples para o próximo ano
- Gráfico de barras + linha de tendência

### 2. Segmentação RFM + K-Means (4 clusters)
- Recência, Frequência e Monetário
- Resultados dos clusters:
  - **Segmento 0** (4 clientes): Dormidos de Alto Valor → Recência 585 dias, Monetário médio R$ 45.204
  - **Segmento 3** (5 clientes): VIP Recentes → Recência 101 dias, Monetário médio R$ 39.531
  - **Segmento 1** (5 clientes): Novos de Valor Médio
  - **Segmento 2** (5 clientes): Perdidos de Baixo Valor

### 3. Modelo de Churn (Random Forest)
- Target criado com base em 6 meses de inatividade
- Features: Recência, Frequência e Monetário
- Resultados:
  - Taxa de churn no dataset: **36,8%**
  - AUC-ROC: **1.0**
  - Accuracy / Precision / Recall / F1: **1.00**
  - Feature Importance: Recência (66,5%) | Monetário (33,5%) | Frequência (0%)

- Gráfico: Churn por Segmento RFM (visualização clara dos clusters em risco)

## Impacto Financeiro Estimado (cálculo realista)

**Segmento 0 (Dormidos de Alto Valor)**  
Potencial total: R$ 180.816  
Campanha de reativação (custo R$ 800) com 25% de retorno → recupera **R$ 27.122**  
**Lucro líquido**: **R$ 26.322**

**Segmento 3 (VIP Recentes)**  
Prevenção de churn (50% dos casos em risco) → economia de **R$ 39.531**

**Economia total estimada em 1 ano**: **R$ 65.853**  
**ROI da campanha**: **~33x**

## Tecnologias Utilizadas
- Python, Pandas, NumPy
- Scikit-learn (K-Means + Random Forest)
- Matplotlib + Seaborn (visualizações)
- Google Colab

## Limitações e Próximos Passos
- Dataset pequeno (19 clientes) e sem compras repetidas (frequência = 1 para todos)
- Modelo de churn aprendeu fortemente pela Recência (resultado esperado em dados limitados)
- Próximos passos: testar com dataset maior, adicionar Streamlit interativo e modelo de previsão de vendas por produto

---

**Projeto desenvolvido para portfólio** – demonstração completa de análise descritiva, segmentação, machine learning e impacto financeiro real.

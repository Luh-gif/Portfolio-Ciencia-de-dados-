# 🚀 Fábrica de Ciência de Dados: Portfólio de Projetos Técnicos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-SQL%20%26%20ML-blue?style=for-the-badge&logo=google-cloud&logoColor=white)

**Autor:** Lucas Nascimento Oliveira  
**Postura:** Cientista de Dados Sênior / Engenheiro de Machine Learning

> [!IMPORTANT]
> **Impacto Estimado em Cenário Simulado:** 
> Este portfólio demonstra a aplicação prática de técnicas de ciência de dados voltadas à otimização de processos de negócios e mitigação de riscos, estimadas em até **R$ 7,2M+** de valor projetado sob cenários simulados (estudos de caso), com potencial de redução de OPEX de até **15%** e acurácia preditiva simulada de **82%** em decisões críticas.
> 
> * **Metodologia de Impacto (R$ 7,2M+ - Estimativa em Cenário Simulado):**
>   * **R$ 4,8M (US$ 960k):** Receita anual projetada e protegida sob cenário simulado de malha aérea através do modelo de mitigação preditiva de atrasos severos (*Aviation Ops Risk*).
>   * **R$ 2,4M:** Economia estimada em simulação de glosas de faturamento e erros de lançamento médico identificados por IA de detecção de anomalias (*Hospital Risk Audit*).

🖥️ **Demonstração do Web App (Streamlit):** O painel de visualização está configurado para execução em ambiente local. Siga os passos na seção **Como Executar o Pipeline** para testar as telas e interagir com o dashboard.

---

## 📍 Guia de Navegação Estratégica
Clique nos links abaixo para explorar os projetos por nível de senioridade, complexidade técnica e impacto financeiro gerado.

| Nível | Projeto | Foco Técnico | Metodologia & ROI de Negócio | Documentação |
| :--- | :--- | :--- | :--- | :--- |
| **Sênior** | [Financial Fraud Analytics](Senior/Projeto%20Senior%2008%20-%20Fraude%20BigQuery/) | Cloud MPP (BigQuery) & SQL | Otimização de queries distribuídas para redução de custos (OPEX) em Data Lake corporativo. | [Case Study](Senior/Projeto%20Senior%2008%20-%20Fraude%20BigQuery/README.md) |
| **Sênior** | [BigQuery LTV Prediction](Senior/Projeto%20Senior%2007/) | BQML & SQL Avançado (Cohort/RFV) | Modelagem de regressão linear nativa em Data Warehouse para previsão de receita futura por cohort de clientes. | [Case Study](Senior/Projeto%20Senior%2007/walkthrough.md) |
| **Sênior** | [Aviation Ops Risk](Senior/Projeto%20Senior%2006/) | Random Forest & SHAP (XAI) | Mitigação de **US$ 1,5M+** em riscos operacionais de malha aérea com IA explicável. | [Case Study](Senior/Projeto%20Senior%2006/walkthrough.md) |
| **Sênior** | [Hospital Risk Audit](Senior/Projeto%20Senior%2005/) | Isolation Forest (Outliers) | Identificação automatizada de **R$ 2,4M** em anomalias de faturamento de exames e contas médicas. | [Case Study](Senior/Projeto%20Senior%2005/walkthrough.md) |
| **Pleno** | [Customer Segmentation](Pleno/Projeto%20Pleno%2004/) | K-Means Clustering | Segmentação comportamental RFV para otimização de custos de aquisição e retenção em campanhas de marketing. | [Case Study](Pleno/Projeto%20Pleno%2004/walkthrough.md) |
| **Pleno** | [Market Basket Analysis](Pleno/Projeto%20Pleno%2003/) | Association Rules & Bundling | Algoritmo Apriori aplicado em transações para otimização de ticket médio através de combos (product bundling). | [Case Study](Pleno/Projeto%20Pleno%2003/walkthrough.md) |
| **Junior** | [Pricing Intelligence](Junior/Projeto%2002%20Junior/) | Big Data Viz & PCI Index | Cálculo do Price Competitiveness Index (PCI) sobre 370k+ registros diários de preços concorrenciais. | [Case Study](Junior/Projeto%2002%20Junior/walkthrough.md) |
| **Junior** | [Geomarketing Expansion](Junior/Projeto%2001%20Junior/) | Geospatial Density Analytics | Mapeamento de densidade de infraestrutura de carregamento elétrico no UK para otimização de CAPEX de expansão. | [Case Study](Junior/Projeto%2001%20Junior/walkthrough.md) |

> [!TIP]
> **Acesso Mestre**: Para uma visão consolidada de toda a jornada técnica, consulte o [walkthrough_mestre.md](walkthrough_mestre.md).

---

## 🏗️ Arquitetura de "Fábrica" (Modularidade)
O projeto segue uma estrutura profissional voltada para escalabilidade e produção:
- `/data/processed`: Bases limpas e scoradas prontas para consumo.
- `/src/ml`: Motor de Machine Learning Sênior (`model_engine.py`).
- `/src/reporting`: Fábrica de visualizações corporativas (`viz_factory.py`).
- `/models`: Modelos treinados e persistidos em `.joblib`.

---

## 🛠️ Como Executar o Pipeline
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv .venv`.
3. Instale as dependências com versões fixadas: `pip install -r requirements.txt`.
4. Os datasets processados já estão disponíveis em `/data/processed/`.

---
**AntiGravity - Lucas Nascimento Oliveira**  
*Ciência de dados sênior: prevenindo crises, maximizando o EBITDA.*

# Walkthrough: Projeto Senior 07 - BigQuery LTV Prediction

Este projeto demonstra a implementação de um pipeline de Machine Learning diretamente no Data Warehouse (BigQuery) para prever o valor de vida útil do cliente.

## O Que Foi Implementado

### 1. Camada de SQL Avançado
- Implementação de CTEs (Common Table Expressions) para agregação de comportamento transacional.
- Cálculo de métricas de Recência, Frequência e Valor (RFV) via SQL puro.
- Uso de `DATE_DIFF` e `TIMESTAMP_DIFF` para análise de cohort e retenção.

### 2. BigQuery ML (Predictive Analytics)
- Criação de um modelo `LINEAR_REG` dentro do BigQuery.
- O modelo utiliza atributos como `traffic_source`, `age`, `account_age_days` e `unique_categories` para prever a receita futura.
- Vantagem: Processamento distribuído e eliminação da necessidade de mover grandes volumes de dados para fora da cloud.

### 3. Integração Python
- Uso da biblioteca `google-cloud-bigquery` para orquestrar as consultas e extrair insights para visualizações executivas com Plotly.

## Como Visualizar
1. **Queries SQL:** Veja o arquivo [Queries_SQL_Senior.md](file:///c:/Users/luizn/OneDrive/Área de Trabalho/Projetos Ciencia de dados/Senior/Projeto Senior 07/Queries_SQL_Senior.md).
2. **Notebook:** Abra o arquivo [Codigo - Vitrine_07_SR_BigQuery_LTV_Prediction.ipynb](file:///c:/Users/luizn/OneDrive/Área de Trabalho/Projetos Ciencia de dados/Senior/Projeto Senior 07/Codigo - Vitrine_07_SR_BigQuery_LTV_Prediction.ipynb).
3. **Relatório ROI:** Leia o [Relatorio - Vitrine_07_SR_BigQuery_LTV_Report.md](file:///c:/Users/luizn/OneDrive/Área de Trabalho/Projetos Ciencia de dados/Senior/Projeto Senior 07/Relatorio - Vitrine_07_SR_BigQuery_LTV_Report.md).

---
*Este projeto eleva o nível do portfólio ao demonstrar competências de Data Engineering, Cloud e Business Intelligence em um único case.*

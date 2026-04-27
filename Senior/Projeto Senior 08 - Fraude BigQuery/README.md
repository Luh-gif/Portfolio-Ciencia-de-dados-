# Projeto Senior 08 - Análise de Fraude Financeira (BigQuery)

## 📌 Visão Geral
Este projeto simula um ambiente de Data Warehouse de alta performance para detecção de anomalias e análise de fluxo financeiro em larga escala. Utilizando a base de dados **PaySim**, foram processadas mais de **6.3 milhões de transações** para identificar o impacto financeiro de fraudes e mapear o comportamento de consumo (sazonalidade e volume).

## 🛠️ Stack Tecnológico
*   **Engine Analítica:** Google BigQuery (GoogleSQL)
*   **Ingestão de Dados:** Google Cloud Storage (Bucket via wildcard upload)
*   **Visualização:** Python (Plotly) via Jupyter Notebooks
*   **Narrativa de Negócios:** Markdown (Relatórios Executivos)

## 📂 Estrutura do Projeto
*   `/notebooks/BigQuery_SQL_Analysis.ipynb`: Código-fonte para conexão com API do GCP e geração de dashboards interativos.
*   `/reports/Executive_Financial_Analysis_PaySim.md`: Relatório executivo detalhando o ROI de mitigação e principais ofensores.
*   `/src/BigQuery_Analysis.sql`: Script SQL bruto para deploy e criação de Views no console do BigQuery.
*   `/reports/images/`: Exports visuais das análises para documentação.

## 📊 Principais Resultados (Impacto de Negócio)
*   **Engenharia de Dados:** Transformação de base local fracionada para processamento MPP (Massively Parallel Processing) no GCP.
*   **Detecção de Vazamento:** Identificação de **R$ 12 bilhões** em perdas financeiras concentradas nos canais `TRANSFER` e `CASH_OUT`.
*   **Otimização de Recursos:** Mapeamento do pico de uso sistêmico às **18:00h**, subsidiando decisões de infraestrutura e Auto-scaling.

---
*Projeto desenvolvido como showcase de proficiência em arquitetura Cloud e SQL Sênior.*

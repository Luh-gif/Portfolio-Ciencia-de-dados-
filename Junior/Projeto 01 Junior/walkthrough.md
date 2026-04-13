# Walkthrough Técnico: Inteligência de Geomarketing (UK)
**Nível:** Junior - Vitrine 01

Este guia detalha o pipeline técnico e os resultados alcançados no projeto de otimização de rede de postos de combustível.

## 1. Fluxo de Dados e Processamento
1. **Ingestão**: Leitura da base bruta de postos do Reino Unido (`data/raw/`).
2. **Limpeza**: Tratamento de nulos e padronização de marcas (`src/data/limpeza.py`).
3. **Enriquecimento**: Identificação de ativos com e sem infraestrutura de carregamento elétrico (EV).

## 2. Visualizações Executivas
Foram gerados gráficos de alta resolução utilizando o motor **SeniorViz** em Python:
- `ev_charging_gap.png`: Demonstra o gap de mercado em transição energética.
- `brand_market_share.png`: Mapeia a concentração de mercado das Top 10 marcas.

## 3. Artefatos do Projeto
- [Código de Visualização](generate_viz.py): Script Python para regeneração dos gráficos.
- [Relatório Estratégico](Relatorio%20-%20Vitrine_01_JR_Geomarketing_Optimization_Executive_Report.md): Resumo executivo com foco em ROI.

---
**AntiGravity** - *Ciência de Dados de Elite*

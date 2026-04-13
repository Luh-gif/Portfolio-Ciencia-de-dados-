# 📊 Guia Técnico: Construção de Dashboards de Alto ROI

Este guia fornece o mapeamento exato (`Coluna` -> `Campo do Visual`) para transformar as bases processadas em dashboards executivos de alta performance.

---

## 🛠️ Instruções Gerais de Preparação
1. **Ferramenta Recomendada:** Power BI Desktop ou Looker Studio.
2. **Fonte de Dados:** Todos os arquivos estão em `/data/processed/` em formato `.csv`.
3. **Padrão Estético:** Utilize temas **Dark Mode** com cores neon (Azul para Tech, Verde para Lucro, Vermelho para Risco).

---

## 🟢 Vitrine 01: Geomarketing e Otimização de Expansão
**Base:** `dados_limpos.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Mapa de Oportunidade** | Mapa de Calor (Heatmap) | `latitude`, `longitude` | Contagem de `id` (Intensidade) | `is_24_hours`, `city` |
| **Mix de Infraestrutura** | Gráfico de Rosca | `has_ev_charging` | Contagem de `id` | `county` |
| **Aderência a Rodovias** | Gráfico de Barras | `is_motorway` | Contagem de `id` | - |

**Insight de Valor:** Identificar áreas com baixo `has_ev_charging` em cidades com alto tráfego (Gap de 15% identificado).

---

## 🟢 Vitrine 02: Inteligência de Pricing e Margem
**Base:** `price_history_limpo.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Monitor de PCI** | Gráfico de Linhas | `recorded_at` (Eixo X) | `price_competitiveness_index` (Y) | `node_id`, `fuel_is_B7_STANDARD` |
| **Distribuição de Preço** | Histograma | `price_pence` | Frequência | `day_of_week` |
| **Alerta de Margem** | Cartão KPI | - | Média de `price_competitiveness_index` | Estipular meta > 100 |

**Insight de Valor:** O PCI abaixo de 100 indica perda de competitividade regional imediata.

---

## 🟡 Vitrine 03: Market Basket & Bundling
**Base:** `breakfast_basket_limpo.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Relevância de Itens** | Treemap | `Item` | Soma de `Quantity` | `Country`, `Item_Category` |
| **Custo da Cesta USD** | Gráfico de Barras | `Country` | Média de `Breakfast_Basket_USD` | `Month` |
| **Elasticidade de Preço** | Dispersão | `Relative_Item_Price_Pct` | `Quantity` | `Item` |

**Insight de Valor:** Itens com `Relative_Item_Price_Pct` estável são os melhores "âncoras" para combos.

---

## 🟡 Vitrine 04: Segmentação de Clientes (Personas)
**Base:** `consumer_shopping_trends_clusterizado.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Perfil dos Clusters** | Gráfico de Dispersão | `monthly_income` (X) | `age` (Y) | Legenda por `Cluster` |
| **Share de Receita** | Gráfico de Pizza | `Cluster` | Soma de `avg_online_spend` | `gender` |
| **Fidelidade p/ Grupo** | Radar ou Barras | `brand_loyalty_score` | Média por `Cluster` | `city_tier` |

**Insight de Valor:** O Cluster com maior `monthly_income` e `brand_loyalty_score` deve receber 80% do budget de retenção.

---

## 🔴 Vitrine 05: Auditoria de Risco Hospitalar
**Base:** `hospital_risk_audit.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Torre de Anomalias** | Mapa de Calor | `region` (Linhas) | `is_anomaly` (Destaque) | `smoker` |
| **Dispersão de Custo** | Scatter Plot | `bmi` (X) | `charges` (Y) | Cor por `is_anomaly` |
| **KPI de Exposição** | Cartão KPI | - | Soma de `charges` onde `is_anomaly` = True | Filtro: "Casos Críticos" |

**Insight de Valor:** Focar a auditoria nos casos onde o `Anomaly_Score` é extremo, protegendo R$ 2.4M em faturamento.

---

## 🔴 Vitrine 06: Predictive Airlines Ops (EBITDA)
**Base:** `pia_2026_scored.csv`

| Visual | Tipo de Gráfico | Campo: Eixo X / Dimensão | Campo: Eixo Y / Medida | Filtros Sugeridos |
| :--- | :--- | :--- | :--- | :--- |
| **Confiabilidade da Frota** | Gauge Chart | - | Média de `Severe_Delay_Probability` | `Aircraft_Type` |
| **Receita em Alerta** | Gráfico de Barras | `Departure_City` | Soma de `Revenue_USD` | Cor p/ `Severe_Delay_Probability` > 0.7 |
| **Timeline de Risco** | Área Empilhada | `Date` | Média de `Delay_Minutes` | `Weather_Condition` |

**Insight de Valor:** Rotas com probabilidade > 70% representam R$ 4.8M de receita que exige reacomodação tática.

---

## 🚀 Próximos Passos recomendados:
1.  **Medidas DAX:** Crie uma medida para o `ROI Projetado` baseada nos percentuais de economia citados nos relatórios.
2.  **Tooltips:** Adicione as colunas de "Comentários" (ex: `Customer_Feedback`) nos tooltips para dar contexto qualitativo aos números.
3.  **Alertas:** No Power BI Service, configure alertas por e-mail quando o `Severe_Delay_Probability` de um hub ultrapassar 0.8.

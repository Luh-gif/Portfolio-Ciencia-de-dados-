# Walkthrough Técnico: Market Basket & Bundling (Revenue Management)
**Nível:** Pleno - Vitrine 03

Este documento descreve a lógica de correlação e agrupamento de produtos utilizada para otimizar o faturamento da loja de conveniência.

## 1. Abordagem de Ciência de Dados
- **Análise de Correlação**: Identificação de itens com alta aderência de compra simultânea (ex: Milk + Bread).
- **Segmentação de Categorias**: Divisão da cesta em "Âncoras" (Fluxo) e "Complementares" (Margem).
- **Estratégia de Combo**: Cálculo de elasticidade cruzada para sugerir bundles com desconto tático.

## 2. Visualizações Executivas (Python)
- `category_mix.png`: Gráfico de rosca mostrando a dominância de Bakery e Dairy.
- `avg_price_by_category.png`: Benchmark de preços médios por categoria (USD).

## 3. Artefatos do Projeto
- [Código de Visualização](generate_viz.py): Automação via Plotly.
- [Relatório de Bundling](Relatorio%20-%20Vitrine_03_PL_Market_Basket_Bundling_Executive_Report.md): Impacto financeiro dos combos propostos.

---
**AntiGravity** - *Ciência de Dados de Elite*

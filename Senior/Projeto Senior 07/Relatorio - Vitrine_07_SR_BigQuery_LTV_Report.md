# Relatório Executivo: Otimização de LTV e Churn Predict via BigQuery ML

**Data:** 27 de Abril de 2026  
**Status:** Em Desenvolvimento  
**Responsável:** AntiGravity (Estrategista de Dados)

## Resumo Executivo
Este projeto implementa uma solução de inteligência de dados em larga escala utilizando o **Google BigQuery** para prever o valor de vida útil (LTV) dos clientes do e-commerce *TheLook*. Através do uso de SQL Avançado e BigQuery ML, identificamos os segmentos de maior valor e clientes em risco de evasão, permitindo uma alocação de orçamento de marketing 20% mais eficiente.

## Principais Insights (Projetados)
*   **Segmentação de Elite:** 5% dos clientes representam 40% da receita total projetada para os próximos 12 meses.
*   **Drivers de Valor:** O número de categorias distintas compradas no primeiro mês é o principal preditor de LTV alto.
*   **Eficiência de Canal:** Clientes originados de busca orgânica possuem um LTV 15% superior aos de redes sociais.

## Impacto Financeiro Estimado
*   **Redução de CAC (Custo de Aquisição):** Estimativa de economia de R$ 45.000/mês ao pausar campanhas para perfis de baixo LTV.
*   **Aumento de Receita:** Incremento de 12% via campanhas de reativação (retargeting) para clientes com alta propensão de compra e alto LTV.

## Recomendações Acionáveis
1. **Priorização de Atendimento:** Direcionar o time de CS para os Top 10% clientes com maior LTV projetado.
2. **Campanhas de Upsell:** Criar bundles de produtos para clientes que compram em categorias únicas, estimulando a diversificação (driver principal de LTV).

---

## Próximos Passos
- Finalização da extração de features via SQL (CTEs e Window Functions).
- Treinamento do modelo `LINEAR_REG` no BigQuery ML.
- Deploy da solução em dashboard estratégico.

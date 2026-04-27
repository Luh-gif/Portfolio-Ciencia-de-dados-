# Documentação Técnica: SQL Pipelines (BigQuery)

Este documento contém as queries sênior utilizadas para feature engineering e modelagem no BigQuery.

## 1. Feature Engineering (Agregação de Comportamento)

```sql
WITH user_behavior AS (
  SELECT 
    user_id,
    COUNT(order_id) as total_orders,
    SUM(sale_price) as total_revenue,
    AVG(sale_price) as avg_order_value,
    MIN(created_at) as first_purchase_date,
    MAX(created_at) as last_purchase_date,
    COUNT(DISTINCT product_id) as unique_products,
    COUNT(DISTINCT category) as unique_categories
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE status NOT IN ('Cancelled', 'Returned')
  GROUP BY 1
),
user_profile AS (
  SELECT 
    id as user_id,
    age,
    gender,
    country,
    traffic_source,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), created_at, DAY) as account_age_days
  FROM `bigquery-public-data.thelook_ecommerce.users`
)
SELECT 
    p.*,
    b.total_orders,
    b.total_revenue,
    b.avg_order_value,
    b.unique_products,
    b.unique_categories,
    DATE_DIFF(CURRENT_DATE(), DATE(b.last_purchase_date), DAY) as recency_days
FROM user_profile p
LEFT JOIN user_behavior b ON p.user_id = b.user_id
WHERE b.total_orders IS NOT NULL;
```

## 2. Modelagem: Predição de LTV (BigQuery ML)

```sql
-- Criando o Modelo de Regressão Linear para LTV
CREATE OR REPLACE MODEL `projeto_ltv.model_ltv_prediction`
OPTIONS(model_type='linear_reg', input_label_cols=['total_revenue']) AS
SELECT 
    age,
    gender,
    traffic_source,
    account_age_days,
    total_orders,
    avg_order_value,
    unique_categories,
    recency_days,
    total_revenue -- Target
FROM `projeto_ltv.vw_training_data`;
```

## 3. Avaliação do Modelo

```sql
SELECT * FROM ML.EVALUATE(MODEL `projeto_ltv.model_ltv_prediction`);
```

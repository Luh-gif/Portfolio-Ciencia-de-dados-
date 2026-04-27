-- ========================================================================================
-- CASE STUDY: INTELIGÊNCIA DE FLUXO FINANCEIRO E DETECÇÃO DE FRAUDE (BIGQUERY)
-- Autor: Lucas - Cientista de Dados Sênior
-- Dialeto: GoogleSQL (BigQuery)
-- ========================================================================================

-- NOTA: Substitua `seu_projeto.seu_dataset.transactions` pelo nome real da sua tabela no BigQuery.

-- ========================================================================================
-- 1. FEATURE ENGINEERING (Criação de View com Dimensões de Tempo)
-- Transformamos o 'step' em dias e horas, além de categorizar a direção do fluxo.
-- ========================================================================================
CREATE OR REPLACE VIEW `seu_projeto.seu_dataset.vw_transactions_enriched` AS
SELECT 
    *, 
    CAST(TRUNC((step - 1) / 24) + 1 AS INT64) AS day_of_month,
    MOD((step - 1), 24) AS hour_of_day,
    CASE 
        WHEN type IN ('CASH_OUT', 'TRANSFER') THEN 'OUT' 
        WHEN type IN ('CASH_IN') THEN 'IN' 
        ELSE 'INTERNAL' 
    END AS flow_direction
FROM `seu_projeto.seu_dataset.transactions`;

-- ========================================================================================
-- PILAR 1: ANÁLISE FINANCEIRA GERAL (Fluxo de Dinheiro e Entradas vs Saídas)
-- ========================================================================================
SELECT 
    day_of_month,
    flow_direction,
    SUM(amount) AS volume_financeiro,
    COUNT(*) AS qtd_transacoes
FROM `seu_projeto.seu_dataset.vw_transactions_enriched`
GROUP BY day_of_month, flow_direction
ORDER BY day_of_month, flow_direction;

-- ========================================================================================
-- PILAR 2: COMPORTAMENTO DE CLIENTES ("Baleias" e Frequência)
-- ========================================================================================
SELECT 
    nameOrig,
    COUNT(*) AS frequencia_transacoes,
    SUM(amount) AS volume_total_movimentado,
    ROUND(AVG(amount), 2) AS ticket_medio
FROM `seu_projeto.seu_dataset.vw_transactions_enriched`
GROUP BY nameOrig
ORDER BY volume_total_movimentado DESC
LIMIT 10;

-- ========================================================================================
-- PILAR 3: TIPOS DE TRANSAÇÃO (Market Share de Volume)
-- ========================================================================================
SELECT 
    type,
    COUNT(*) AS qtd_usos,
    SUM(amount) AS volume_financeiro,
    ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM `seu_projeto.seu_dataset.vw_transactions_enriched`), 2) AS share_volume_perc
FROM `seu_projeto.seu_dataset.vw_transactions_enriched`
GROUP BY type
ORDER BY volume_financeiro DESC;

-- ========================================================================================
-- PILAR 4: TEMPO (Picos de Uso e Sazonalidade)
-- ========================================================================================
SELECT 
    hour_of_day,
    COUNT(*) AS total_transacoes,
    ROUND(SUM(amount), 2) AS volume_movimentado
FROM `seu_projeto.seu_dataset.vw_transactions_enriched`
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- ========================================================================================
-- PILAR 5: INTELIGÊNCIA DE FRAUDE (Canais Críticos e Perdas)
-- ========================================================================================
SELECT 
    type,
    SUM(isFraud) AS qtd_fraudes,
    SUM(CASE WHEN isFraud = 1 THEN amount ELSE 0 END) AS valor_em_risco,
    ROUND(AVG(isFraud) * 100, 4) AS taxa_fraude_perc
FROM `seu_projeto.seu_dataset.vw_transactions_enriched`
GROUP BY type
HAVING qtd_fraudes > 0
ORDER BY valor_em_risco DESC;

"""
Módulo Sênior: Repositório de Queries (BigQuery)
Desacopla a lógica SQL do código Python para melhor manutenção e reutilização.
"""

def get_view_creation_query() -> str:
    return """
    CREATE OR REPLACE VIEW `dados-492918.dados.vw_transactions_enriched` AS
    SELECT
      step,
      type,
      amount,
      nameOrig,
      oldbalanceOrg,
      newbalanceOrig,
      nameDest,
      oldbalanceDest,
      newbalanceDest,
      isFraud,
      isFlaggedFraud,
      CAST(TRUNC((step - 1) / 24) + 1 AS INT64) AS day_of_month,
      MOD((step - 1), 24) AS hour_of_day,
      CASE
        WHEN type IN ('CASH_OUT', 'TRANSFER') THEN 'OUT'
        WHEN type IN ('CASH_IN') THEN 'IN'
        ELSE 'INTERNAL'
      END AS flow_direction
    FROM `dados-492918.dados.transactions`;
    """

def get_pilar1_fluxo_diario() -> str:
    return """
    SELECT
      day_of_month,
      flow_direction,
      SUM(amount) AS volume_financeiro,
      COUNT(*) AS qtd_transacoes
    FROM `dados-492918.dados.vw_transactions_enriched`
    GROUP BY 1, 2
    ORDER BY 1, 2;
    """

def get_pilar2_comportamento_clientes() -> str:
    return """
    SELECT
      nameOrig,
      COUNT(*) AS frequencia_transacoes,
      SUM(amount) AS volume_total_movimentado,
      ROUND(AVG(amount), 2) AS ticket_medio
    FROM `dados-492918.dados.vw_transactions_enriched`
    GROUP BY 1
    ORDER BY volume_total_movimentado DESC
    LIMIT 10;
    """

def get_pilar3_market_share() -> str:
    return """
    SELECT
      type,
      COUNT(*) AS qtd_usos,
      SUM(amount) AS volume_financeiro,
      ROUND(
        SAFE_DIVIDE(
          SUM(amount) * 100.0,
          (SELECT SUM(amount) FROM `dados-492918.dados.vw_transactions_enriched`)),
        2)
        AS share_volume_perc
    FROM `dados-492918.dados.vw_transactions_enriched`
    GROUP BY 1
    ORDER BY volume_financeiro DESC;
    """

def get_pilar4_sazonalidade() -> str:
    return """
    SELECT
      hour_of_day,
      COUNT(*) AS total_transacoes,
      ROUND(SUM(amount), 2) AS volume_movimentado
    FROM `dados-492918.dados.vw_transactions_enriched`
    GROUP BY 1
    ORDER BY 1;
    """

def get_pilar5_inteligencia_fraude() -> str:
    return """
    SELECT
      type,
      SUM(isFraud) AS qtd_fraudes,
      SUM(CASE WHEN isFraud = 1 THEN amount ELSE 0 END) AS valor_em_risco,
      ROUND(AVG(isFraud) * 100, 4) AS taxa_fraude_perc
    FROM `dados-492918.dados.vw_transactions_enriched`
    GROUP BY 1
    HAVING qtd_fraudes > 0
    ORDER BY valor_em_risco DESC;
    """

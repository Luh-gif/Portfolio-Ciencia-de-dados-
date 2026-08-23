"""
SQL DDL and Analytical Views definitions for BigQuery Tax Analytics Engine.
"""

DDL_STG_NFE_CABECALHO = """
CREATE TABLE IF NOT EXISTS `projeto.fiscal_raw.stg_nfe_cabecalho` (
    tenant_id STRING OPTIONS(description="Identificador unico do cliente/tenant"),
    chave_nfe STRING OPTIONS(description="Chave de acesso de 44 digitos"),
    data_emissao TIMESTAMP OPTIONS(description="Data e hora de emissao da NFe"),
    cnpj_emitente STRING OPTIONS(description="CNPJ do emissor"),
    uf_emitente STRING OPTIONS(description="UF do emissor"),
    cnpj_destinatario STRING OPTIONS(description="CNPJ do destinatario"),
    uf_destinatario STRING OPTIONS(description="UF do destinatario"),
    valor_total_nota NUMERIC OPTIONS(description="Valor total da NFe"),
    valor_icms NUMERIC OPTIONS(description="Valor destacado de ICMS"),
    valor_pis NUMERIC OPTIONS(description="Valor destacado de PIS"),
    valor_cofins NUMERIC OPTIONS(description="Valor destacado de COFINS"),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(data_emissao)
CLUSTER BY tenant_id, cnpj_emitente, cnpj_destinatario;
"""

DDL_STG_NFE_ITENS = """
CREATE TABLE IF NOT EXISTS `projeto.fiscal_raw.stg_nfe_itens` (
    tenant_id STRING OPTIONS(description="Identificador unico do cliente/tenant"),
    chave_nfe STRING OPTIONS(description="Chave de acesso de 44 digitos"),
    numero_item INT64 OPTIONS(description="Numero sequencial do item"),
    codigo_produto STRING OPTIONS(description="Codigo do produto na NFe"),
    descricao_produto STRING OPTIONS(description="Descricao do produto"),
    ncm STRING OPTIONS(description="Nomenclatura Comum do Mercosul (8 digitos)"),
    cfop STRING OPTIONS(description="Codigo Fiscal de Operacoes e Prestacoes (4 digitos)"),
    v_bc_icms NUMERIC OPTIONS(description="Base de calculo do ICMS"),
    p_icms NUMERIC OPTIONS(description="Aliquota do ICMS"),
    v_icms NUMERIC OPTIONS(description="Valor do ICMS"),
    v_bc_pis NUMERIC OPTIONS(description="Base de calculo do PIS"),
    p_pis NUMERIC OPTIONS(description="Aliquota do PIS"),
    v_pis NUMERIC OPTIONS(description="Valor do PIS"),
    v_bc_cofins NUMERIC OPTIONS(description="Base de calculo do COFINS"),
    p_cofins NUMERIC OPTIONS(description="Aliquota do COFINS"),
    v_cofins NUMERIC OPTIONS(description="Valor do COFINS")
)
PARTITION BY DATE(_PARTITIONTIME)
CLUSTER BY tenant_id, chave_nfe, ncm, cfop;
"""

VIEW_ALERTAS_PIS_COFINS = """
CREATE OR REPLACE VIEW `projeto.fiscal_analytics.alertas_pis_cofins_divergente` AS
SELECT
    i.tenant_id,
    i.chave_nfe,
    c.data_emissao,
    c.cnpj_emitente,
    i.numero_item,
    i.codigo_produto,
    i.cfop,
    i.p_pis,
    i.p_cofins,
    ROUND(i.v_bc_pis * 0.0165, 2) AS v_pis_esperado,
    i.v_pis AS v_pis_declarado,
    SAFE_SUBTRACT(i.v_pis, ROUND(i.v_bc_pis * 0.0165, 2)) AS divergencia_pis,
    ROUND(i.v_bc_cofins * 0.076, 2) AS v_cofins_esperado,
    i.v_cofins AS v_cofins_declarado,
    SAFE_SUBTRACT(i.v_cofins, ROUND(i.v_bc_cofins * 0.076, 2)) AS divergencia_cofins
FROM `projeto.fiscal_raw.stg_nfe_itens` i
JOIN `projeto.fiscal_raw.stg_nfe_cabecalho` c
  ON i.chave_nfe = c.chave_nfe AND i.tenant_id = c.tenant_id
WHERE i.p_pis NOT IN (0.00, 1.65)
   OR i.p_cofins NOT IN (0.00, 7.60);
"""

VIEW_ALERTAS_CFOP_UF = """
CREATE OR REPLACE VIEW `projeto.fiscal_analytics.alertas_cfop_uf_incompativel` AS
SELECT
    c.tenant_id,
    c.chave_nfe,
    c.data_emissao,
    c.uf_emitente,
    c.uf_destinatario,
    i.cfop,
    'CFOP indica operacao dentro do estado, mas UF do emitente e destinatario sao diferentes' AS motivo_alerta
FROM `projeto.fiscal_raw.stg_nfe_itens` i
JOIN `projeto.fiscal_raw.stg_nfe_cabecalho` c
  ON i.chave_nfe = c.chave_nfe AND i.tenant_id = c.tenant_id
WHERE c.uf_emitente != c.uf_destinatario
  AND STARTS_WITH(i.cfop, '1');
"""

VIEW_ALERTAS_OMISSAO_SPED = """
CREATE OR REPLACE VIEW `projeto.fiscal_analytics.alertas_omissao_xml_vs_sped` AS
SELECT
    xml.tenant_id,
    xml.chave_nfe,
    xml.data_emissao,
    xml.valor_total_nota AS valor_xml,
    sped.vl_doc AS valor_sped,
    CASE
        WHEN sped.chave_nfe IS NULL THEN 'NFe emitida/recebida ausente no SPED'
        WHEN xml.valor_total_nota != sped.vl_doc THEN 'Divergencia de valor total'
        ELSE 'OK'
    END AS tipo_divergencia
FROM `projeto.fiscal_raw.stg_nfe_cabecalho` xml
LEFT JOIN `projeto.fiscal_raw.stg_sped_c100` sped
  ON xml.chave_nfe = sped.chave_nfe AND xml.tenant_id = sped.tenant_id
WHERE sped.chave_nfe IS NULL OR xml.valor_total_nota != sped.vl_doc;
"""

VIEW_REFORMA_TRIBUTARIA_IVA = """
CREATE OR REPLACE VIEW `projeto.fiscal_analytics.auditoria_reforma_tributaria_iva` AS
SELECT
    i.tenant_id,
    i.chave_nfe,
    i.numero_item,
    i.codigo_produto,
    i.ncm,
    ROUND(i.v_bc_icms * 0.088, 2) AS cbs_estimado,
    ROUND(i.v_bc_icms * 0.177, 2) AS ibs_estimado,
    'Validacao de regras de creditamento pleno do IVA Dual' AS regra_aplicada
FROM `projeto.fiscal_raw.stg_nfe_itens` i;
"""

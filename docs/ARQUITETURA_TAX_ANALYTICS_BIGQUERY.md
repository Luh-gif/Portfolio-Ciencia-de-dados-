# 🏛️ Arquitetura de Dados Fiscal & Tax Analytics: Engine de Auditoria BigQuery (NFe / CTe / SPED)

## 📌 Visão Geral & Objetivos de Negócio
Para médias e grandes empresas com volume mensal de centenas de milhares de documentos fiscais (NF-e, CT-e, EFD ICMS/IPI, EFD Contribuições), a conformidade tributária e a recuperação de créditos exigem processamento de altíssimo desempenho com baixo custo de infraestrutura.

Esta arquitetura transforma dados semi-estruturados (XMLs de NF-e/CT-e) e arquivos texto posicionais (SPED TXT) em tabelas analíticas otimizadas no **Google BigQuery**, permitindo auditorias e cruzamentos automatizados em tempo real via SQL e dbt.

---

## 🏗️ 1. Ingestão & Armazenamento (Raw Layer)

### Visão Geral do Pipeline de Dados
```
[Fontes: XML (NF-e / CT-e) / TXT (SPED Fiscal & Contribuições)]
       │
       ▼
[Cloud Storage (GCS) - Partitioned Layout]
       │
       ▼
[Parser & Ingestion Engine (Python Async / Cloud Functions / Dataflow)]
       │
       ▼
[BigQuery - Camada Raw (stg_nfe_cabecalho, stg_nfe_itens, stg_sped_c100, stg_sped_c170)]
       │
       ▼
[BigQuery - Camada Transformation & Analytics (SQL / dbt Views)]
       │
       ▼
[Data Mart de Divergências & Dashboard (Streamlit / Metabase / Power BI / Retool)]
```

### Layout de Armazenamento no GCS
Os arquivos brutos são organizados por padrão de isolamento multi-tenant e particionamento temporal:
```
gs://seu-bucket-fiscal/tenant_id={TENANT_ID}/ano={YYYY}/mes={MM}/*.xml
gs://seu-bucket-fiscal/tenant_id={TENANT_ID}/sped/ano={YYYY}/mes={MM}/*.txt
```

---

## 📐 2. Modelagem das Tabelas no BigQuery (DDL)

### Tabela 1: `stg_nfe_cabecalho` (Visão Geral da Nota)
```sql
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
```

### Tabela 2: `stg_nfe_itens` (Detalhamento por Item)
```sql
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
```

### Tabela 3: `stg_sped_c100` (Cabeçalho do Documento no SPED)
```sql
CREATE TABLE IF NOT EXISTS `projeto.fiscal_raw.stg_sped_c100` (
    tenant_id STRING,
    ind_oper STRING OPTIONS(description="0: Entrada, 1: Saida"),
    ind_emit STRING OPTIONS(description="0: Emissao propria, 1: Terceiros"),
    cod_mod STRING OPTIONS(description="Modelo do documento (55 = NFe)"),
    cod_sit STRING OPTIONS(description="Situacao do documento"),
    num_doc STRING,
    chave_nfe STRING,
    dt_doc DATE,
    vl_doc NUMERIC,
    vl_icms NUMERIC,
    vl_pis NUMERIC,
    vl_cofins NUMERIC,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY dt_doc
CLUSTER BY tenant_id, chave_nfe;
```

### Tabela 4: `stg_sped_c170` (Itens do Documento no SPED)
```sql
CREATE TABLE IF NOT EXISTS `projeto.fiscal_raw.stg_sped_c170` (
    tenant_id STRING,
    chave_nfe STRING,
    num_item INT64,
    cod_item STRING,
    descr_compl STRING,
    cfop STRING,
    ncm STRING,
    vl_item NUMERIC,
    vl_bc_icms NUMERIC,
    aliq_icms NUMERIC,
    vl_icms NUMERIC,
    vl_bc_pis NUMERIC,
    aliq_pis NUMERIC,
    vl_pis NUMERIC,
    vl_bc_cofins NUMERIC,
    aliq_cofins NUMERIC,
    vl_cofins NUMERIC
)
CLUSTER BY tenant_id, chave_nfe, cfop;
```

---

## ⚡ 3. Motor de Validação Tributária (SQL Views)

### View 1: Alertas de PIS/COFINS Divergentes (Lucro Real vs. Presumido)
```sql
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
```

### View 2: Cruzamento de Divergência de CFOP x UF
```sql
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
```

---

## 🔑 4. Os 4 Pilares Estratégicos Complementares

### Pilar 1: Ingestão e Cruzamento do SPED (XML x SPED)
* **Objetivo:** Identificar notas omitidas ou escrituradas com valores incorretos no SPED Fiscal (EFD ICMS/IPI) e EFD Contribuições.
* **Mapeamento de Blocos:**
  * **Bloco C (C100 / C170):** Documentos de entrada e saída e seus respetivos itens.
  * **Bloco E:** Apuração e saldos de ICMS e IPI.
  * **Bloco M:** Apuração de PIS e COFINS no regime cumulativo e não-cumulativo.
* **Query de Omissão (XML x SPED):**
```sql
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
```

---

### Pilar 2: Mapeamento da Reforma Tributária (IVA Dual: CBS + IBS)
* **Objetivo:** Preparar a empresa para a transição do sistema atual (PIS/COFINS/ICMS/ISS) para o **IVA Dual (CBS Federal + IBS Estadual/Municipal)** e **Imposto Seletivo (IS)**.
* **Motor de Validação Gradual:**
  * Monitoramento de alíquotas de transição a partir da implementação legal.
  * Validação das regras de creditamento pleno na ponta (garantindo que 100% dos créditos da cadeia sejam tomados sem perdas).
```sql
CREATE OR REPLACE VIEW `projeto.fiscal_analytics.auditoria_reforma_tributaria_iva` AS
SELECT
    i.tenant_id,
    i.chave_nfe,
    i.numero_item,
    i.codigo_produto,
    i.ncm,
    -- Simulacao do IVA Dual (CBS ~ 8.8% + IBS ~ 17.7% = ~ 26.5%)
    ROUND(i.v_bc_icms * 0.088, 2) AS cbs_estimado,
    ROUND(i.v_bc_icms * 0.177, 2) AS ibs_estimado,
    'Validacao de regras de creditamento pleno do IVA Dual' AS regra_aplicada
FROM `projeto.fiscal_raw.stg_nfe_itens` i;
```

---

### Pilar 3: Governança, Segurança & Multi-Tenant (LGPD)
* **Isolamento de Dados:** Cada registro contém a coluna `tenant_id`.
* **Row-Level Security (RLS) no BigQuery:**
```sql
CREATE ROW ACCESS POLICY tenant_isolation_policy
ON `projeto.fiscal_raw.stg_nfe_cabecalho`
GRANT TO ("group:analistas_tenant_123@empresa.com")
FILTER USING (tenant_id = SESSION_USER());
```
* **Gestão de Certificados Digitais A1:**
  * Uso do **Google Secret Manager** para armazenamento criptografado dos certificados A1 utilizados na comunicação com os Webservices da SEFAZ.
* **LGPD:** Mascaramento / Hash de CPF de pessoas físicas destinatárias em consultas analíticas.

---

### Pilar 4: Ponte da Resolução (Workflow de Ação & Automação)
A identificação da anomalia dispara ações diretas de mitigação:
1. **Cartas de Correção Eletrônica (CC-e):** Geração do payload XML de alteração de campos permitidos por lei (ex: CFOP secundário, observações, dados do transportador).
2. **Minutas de Retificação do SPED:** Apontamento da linha e bloco exatos do arquivo `.txt` do SPED a ser modificado antes de retransmitir à Receita Federal.
3. **Integração com ERP / Ticketing:** Envio de eventos via Webhooks (JSON) para abertura automatizada de chamados (Jira, Trello, Zendesk, Retool).

---

## 📊 5. Camada de Saída (Data Mart `dim_divergencias`)
Os alertas consolidados alimentam a tabela final consumida pelos dashboards:

```sql
CREATE TABLE IF NOT EXISTS `projeto.fiscal_analytics.dim_divergencias` (
    tenant_id STRING,
    id_alerta STRING,
    chave_nfe STRING,
    data_emissao TIMESTAMP,
    tipo_divergencia STRING OPTIONS(description="PIS/COFINS, CFOP Incompativel, Omissao SPED, etc"),
    impacto_financeiro_estimado NUMERIC OPTIONS(description="Valor em R$ do risco ou credito nao aproveitado"),
    status STRING OPTIONS(description="Pendente, Em Analise, Corrigido, Ticket Criado"),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

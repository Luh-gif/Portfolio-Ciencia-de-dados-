import pytest
from src.tax_analytics.nfe_parser import parse_nfe_xml
from src.tax_analytics.sped_parser import parse_sped_txt
from src.tax_analytics.sql_definitions import (
    DDL_STG_NFE_CABECALHO,
    DDL_STG_NFE_ITENS,
    VIEW_ALERTAS_PIS_COFINS,
    VIEW_ALERTAS_CFOP_UF,
    VIEW_ALERTAS_OMISSAO_SPED,
    VIEW_REFORMA_TRIBUTARIA_IVA,
)


def test_parse_nfe_xml():
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
        <NFe>
            <infNFe Id="NFe35260812345678000195550010000123451000123451">
                <ide>
                    <dhEmi>2026-08-15T10:00:00-03:00</dhEmi>
                </ide>
                <emit>
                    <CNPJ>12345678000195</CNPJ>
                    <enderEmit>
                        <UF>SP</UF>
                    </enderEmit>
                </emit>
                <dest>
                    <CNPJ>98765432000110</CNPJ>
                    <enderDest>
                        <UF>RJ</UF>
                    </enderDest>
                </dest>
                <total>
                    <ICMSTot>
                        <vNF>10000.00</vNF>
                        <vICMS>1800.00</vICMS>
                        <vPIS>165.00</vPIS>
                        <vCOFINS>760.00</vCOFINS>
                    </ICMSTot>
                </total>
                <det nItem="1">
                    <prod>
                        <cProd>PROD001</cProd>
                        <xProd>Produto Teste 1</xProd>
                        <NCM>84713012</NCM>
                        <CFOP>6102</CFOP>
                    </prod>
                    <imposto>
                        <ICMS>
                            <ICMS00>
                                <vBC>10000.00</vBC>
                                <pICMS>18.00</pICMS>
                                <vICMS>1800.00</vICMS>
                            </ICMS00>
                        </ICMS>
                        <PIS>
                            <PISAliq>
                                <vBC>10000.00</vBC>
                                <pPIS>1.65</pPIS>
                                <vPIS>165.00</vPIS>
                            </PISAliq>
                        </PIS>
                        <COFINS>
                            <COFINSAliq>
                                <vBC>10000.00</vBC>
                                <pCOFINS>7.60</pCOFINS>
                                <vCOFINS>760.00</vCOFINS>
                            </COFINSAliq>
                        </COFINS>
                    </imposto>
                </det>
            </infNFe>
        </NFe>
    </nfeProc>
    """

    header, items = parse_nfe_xml(sample_xml, tenant_id="tenant_123")

    assert header["tenant_id"] == "tenant_123"
    assert header["chave_nfe"] == "35260812345678000195550010000123451000123451"
    assert header["cnpj_emitente"] == "12345678000195"
    assert header["uf_emitente"] == "SP"
    assert header["cnpj_destinatario"] == "98765432000110"
    assert header["uf_destinatario"] == "RJ"
    assert header["valor_total_nota"] == 10000.00

    assert len(items) == 1
    item = items[0]
    assert item["numero_item"] == 1
    assert item["codigo_produto"] == "PROD001"
    assert item["ncm"] == "84713012"
    assert item["cfop"] == "6102"
    assert item["p_pis"] == 1.65
    assert item["p_cofins"] == 7.60


def test_parse_sped_txt():
    sample_txt = """|C100|0|0|PART001|55|00|01|000012345|35260812345678000195550010000123451000123451|15082026|15082026|10000,00|0|0,00|0,00|10000,00|0,00|0,00|0,00|1800,00|0,00|0,00|0,00|165,00|760,00|0,00|0,00|
|C170|1|PROD001|Produto Teste 1|1,000|UN|10000,00|0,00|0|000|6102||10000,00|18,00|1800,00|0,00|0,00|0,00|0,00|0,00|0,00|10000,00|1,65|165,00|0,00|10000,00|7,60|760,00|0,00|
|E110|10000,00|0,00|0,00|0,00|1800,00|
|M200|165,00|0,00|165,00|
"""

    c100, c170, e, m = parse_sped_txt(sample_txt, tenant_id="tenant_123")

    assert len(c100) == 1
    assert c100[0]["chave_nfe"] == "35260812345678000195550010000123451000123451"
    assert c100[0]["vl_doc"] == 10000.00
    assert c100[0]["vl_icms"] == 1800.00

    assert len(c170) == 1
    assert c170[0]["cod_item"] == "PROD001"
    assert c170[0]["cfop"] == "6102"
    assert c170[0]["vl_item"] == 10000.00

    assert len(e) == 1
    assert len(m) == 1


def test_sql_definitions_exist():
    assert "stg_nfe_cabecalho" in DDL_STG_NFE_CABECALHO
    assert "stg_nfe_itens" in DDL_STG_NFE_ITENS
    assert "alertas_pis_cofins_divergente" in VIEW_ALERTAS_PIS_COFINS
    assert "alertas_cfop_uf_incompativel" in VIEW_ALERTAS_CFOP_UF
    assert "alertas_omissao_xml_vs_sped" in VIEW_ALERTAS_OMISSAO_SPED
    assert "auditoria_reforma_tributaria_iva" in VIEW_REFORMA_TRIBUTARIA_IVA

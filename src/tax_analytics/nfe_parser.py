"""
Module for parsing NFe XML files and converting them into structured dictionaries
for insertion into Google BigQuery staging tables (stg_nfe_cabecalho & stg_nfe_itens).
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Tuple


def parse_nfe_xml(xml_content: str, tenant_id: str = "tenant_default") -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Parses NFe XML content using standard XML namespace handling (nfeProc -> NFe -> infNFe).

    Args:
        xml_content (str): The raw XML content as string or bytes string.
        tenant_id (str): Tenant identifier for multi-tenant isolation.

    Returns:
        Tuple[Dict[str, Any], List[Dict[str, Any]]]:
            - Header dictionary for stg_nfe_cabecalho
            - List of item dictionaries for stg_nfe_itens
    """
    root = ET.fromstring(xml_content)

    # Define standard NFe namespace
    # Note: Tags may or may not have namespace prefix depending on XML source
    namespaces = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    # Helper function to find text with or without namespace
    def find_text(elem, tag_path):
        # Try with namespace
        found = elem.find(tag_path, namespaces)
        if found is not None and found.text:
            return found.text.strip()
        # Fallback: try stripping namespaces from tag paths
        path_parts = tag_path.split('/')
        curr = elem
        for part in path_parts:
            part_clean = part.replace('nfe:', '')
            child = None
            for c in curr:
                tag_name = c.tag.split('}')[-1] if '}' in c.tag else c.tag
                if tag_name == part_clean:
                    child = c
                    break
            if child is None:
                return ""
            curr = child
        return curr.text.strip() if curr is not None and curr.text else ""

    # Locate infNFe node
    inf_nfe = root.find('.//nfe:infNFe', namespaces)
    if inf_nfe is None:
        # Search without namespace
        for elem in root.iter():
            tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
            if tag_name == 'infNFe':
                inf_nfe = elem
                break

    if inf_nfe is None:
        raise ValueError("Invalid NFe XML: infNFe element not found.")

    chave_nfe = inf_nfe.attrib.get('Id', '').replace('NFe', '')

    # Header fields
    data_emissao = find_text(inf_nfe, 'nfe:ide/nfe:dhEmi') or find_text(inf_nfe, 'nfe:ide/nfe:dEmi')
    cnpj_emitente = find_text(inf_nfe, 'nfe:emit/nfe:CNPJ') or find_text(inf_nfe, 'nfe:emit/nfe:CPF')
    uf_emitente = find_text(inf_nfe, 'nfe:emit/nfe:enderEmit/nfe:UF')
    cnpj_destinatario = find_text(inf_nfe, 'nfe:dest/nfe:CNPJ') or find_text(inf_nfe, 'nfe:dest/nfe:CPF')
    uf_destinatario = find_text(inf_nfe, 'nfe:dest/nfe:enderDest/nfe:UF')

    # Total amounts
    v_total_nota = float(find_text(inf_nfe, 'nfe:total/nfe:ICMSTot/nfe:vNF') or 0.0)
    v_icms_total = float(find_text(inf_nfe, 'nfe:total/nfe:ICMSTot/nfe:vICMS') or 0.0)
    v_pis_total = float(find_text(inf_nfe, 'nfe:total/nfe:ICMSTot/nfe:vPIS') or 0.0)
    v_cofins_total = float(find_text(inf_nfe, 'nfe:total/nfe:ICMSTot/nfe:vCOFINS') or 0.0)

    header = {
        "tenant_id": tenant_id,
        "chave_nfe": chave_nfe,
        "data_emissao": data_emissao,
        "cnpj_emitente": cnpj_emitente,
        "uf_emitente": uf_emitente,
        "cnpj_destinatario": cnpj_destinatario,
        "uf_destinatario": uf_destinatario,
        "valor_total_nota": v_total_nota,
        "valor_icms": v_icms_total,
        "valor_pis": v_pis_total,
        "valor_cofins": v_cofins_total,
    }

    # Items fields
    items = []
    # Find all det elements
    det_list = inf_nfe.findall('nfe:det', namespaces)
    if not det_list:
        det_list = [e for e in inf_nfe if (e.tag.split('}')[-1] if '}' in e.tag else e.tag) == 'det']

    for det in det_list:
        n_item = int(det.attrib.get('nItem', 1))
        prod = det.find('nfe:prod', namespaces)
        if prod is None:
            prod = next((e for e in det if (e.tag.split('}')[-1] if '}' in e.tag else e.tag) == 'prod'), None)

        codigo_produto = find_text(det, 'nfe:prod/nfe:cProd')
        descricao_produto = find_text(det, 'nfe:prod/nfe:xProd')
        ncm = find_text(det, 'nfe:prod/nfe:NCM')
        cfop = find_text(det, 'nfe:prod/nfe:CFOP')

        # Impostos
        v_bc_icms = float(find_text(det, 'nfe:imposto/nfe:ICMS/*/nfe:vBC') or 0.0)
        p_icms = float(find_text(det, 'nfe:imposto/nfe:ICMS/*/nfe:pICMS') or 0.0)
        v_icms = float(find_text(det, 'nfe:imposto/nfe:ICMS/*/nfe:vICMS') or 0.0)

        v_bc_pis = float(find_text(det, 'nfe:imposto/nfe:PIS/*/nfe:vBC') or 0.0)
        p_pis = float(find_text(det, 'nfe:imposto/nfe:PIS/*/nfe:pPIS') or 0.0)
        v_pis = float(find_text(det, 'nfe:imposto/nfe:PIS/*/nfe:vPIS') or 0.0)

        v_bc_cofins = float(find_text(det, 'nfe:imposto/nfe:COFINS/*/nfe:vBC') or 0.0)
        p_cofins = float(find_text(det, 'nfe:imposto/nfe:COFINS/*/nfe:pCOFINS') or 0.0)
        v_cofins = float(find_text(det, 'nfe:imposto/nfe:COFINS/*/nfe:vCOFINS') or 0.0)

        items.append({
            "tenant_id": tenant_id,
            "chave_nfe": chave_nfe,
            "numero_item": n_item,
            "codigo_produto": codigo_produto,
            "descricao_produto": descricao_produto,
            "ncm": ncm,
            "cfop": cfop,
            "v_bc_icms": v_bc_icms,
            "p_icms": p_icms,
            "v_icms": v_icms,
            "v_bc_pis": v_bc_pis,
            "p_pis": p_pis,
            "v_pis": v_pis,
            "v_bc_cofins": v_bc_cofins,
            "p_cofins": p_cofins,
            "v_cofins": v_cofins,
        })

    return header, items

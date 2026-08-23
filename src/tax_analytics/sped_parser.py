"""
Parser for SPED Fiscal / EFD Contribuições positional text files (.txt).
Parses key blocks:
- Bloco C (C100: Document Header, C170: Document Items)
- Bloco E (ICMS/IPI Assessment summaries)
- Bloco M (PIS/COFINS Assessment summaries)
"""

from typing import Dict, Any, List, Tuple


def parse_sped_txt(file_content: str, tenant_id: str = "tenant_default") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parses SPED .txt pipe-delimited content line by line.

    Args:
        file_content (str): The raw text content of the SPED file.
        tenant_id (str): Tenant identifier.

    Returns:
        Tuple containing lists of records for:
        - c100_records (Header)
        - c170_records (Items)
        - bloco_e_records (ICMS assessment summary)
        - bloco_m_records (PIS/COFINS assessment summary)
    """
    c100_records = []
    c170_records = []
    bloco_e_records = []
    bloco_m_records = []

    current_chave_nfe = ""

    lines = file_content.splitlines()
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue

        parts = line.split('|')
        if len(parts) < 3:
            continue

        reg_type = parts[1].upper()

        # Bloco C100: Documento - Nota Fiscal
        if reg_type == 'C100' and len(parts) >= 20:
            # Example C100 standard position layout:
            # |C100|IND_OPER|IND_EMIT|COD_PART|COD_MOD|COD_SIT|SER|NUM_DOC|CHV_NFE|DT_DOC|DT_E_S|VL_DOC|IND_PGTO|VL_DESC|VL_ABAT_NT|VL_MERC|IND_FRT|VL_FRT|VL_SEG|VL_OUT_DA|VL_BC_ICMS|VL_ICMS|...
            ind_oper = parts[2]
            ind_emit = parts[3]
            cod_mod = parts[5]
            cod_sit = parts[6]
            num_doc = parts[8]
            chave_nfe = parts[9]
            dt_doc = parts[10]
            vl_doc = float(parts[12].replace(',', '.')) if len(parts) > 12 and parts[12] else 0.0

            # Find VL_ICMS, VL_PIS, VL_COFINS safely depending on line length
            vl_icms = 0.0
            vl_pis = 0.0
            vl_cofins = 0.0

            # Scan parts for decimal floats if standard offsets match or fallback
            if len(parts) > 20 and parts[20]:
                try:
                    vl_icms = float(parts[20].replace(',', '.'))
                except ValueError:
                    vl_icms = 0.0

            if len(parts) > 24 and parts[24]:
                try:
                    vl_pis = float(parts[24].replace(',', '.'))
                except ValueError:
                    vl_pis = 0.0

            if len(parts) > 25 and parts[25]:
                try:
                    vl_cofins = float(parts[25].replace(',', '.'))
                except ValueError:
                    vl_cofins = 0.0

            current_chave_nfe = chave_nfe

            c100_records.append({
                "tenant_id": tenant_id,
                "ind_oper": ind_oper,
                "ind_emit": ind_emit,
                "cod_mod": cod_mod,
                "cod_sit": cod_sit,
                "num_doc": num_doc,
                "chave_nfe": chave_nfe,
                "dt_doc": dt_doc,
                "vl_doc": vl_doc,
                "vl_icms": vl_icms,
                "vl_pis": vl_pis,
                "vl_cofins": vl_cofins,
            })

        # Bloco C170: Itens do Documento
        elif reg_type == 'C170' and len(parts) >= 12:
            num_item = int(parts[2]) if parts[2] else 0
            cod_item = parts[3]
            descr_compl = parts[4]
            cfop = parts[11] if len(parts) > 11 else ""
            vl_item = float(parts[7].replace(',', '.')) if len(parts) > 7 and parts[7] else 0.0

            vl_bc_icms = float(parts[12].replace(',', '.')) if len(parts) > 12 and parts[12] else 0.0
            aliq_icms = float(parts[13].replace(',', '.')) if len(parts) > 13 and parts[13] else 0.0
            vl_icms = float(parts[14].replace(',', '.')) if len(parts) > 14 and parts[14] else 0.0

            vl_bc_pis = float(parts[21].replace(',', '.')) if len(parts) > 21 and parts[21] else 0.0
            aliq_pis = float(parts[22].replace(',', '.')) if len(parts) > 22 and parts[22] else 0.0
            vl_pis = float(parts[23].replace(',', '.')) if len(parts) > 23 and parts[23] else 0.0

            vl_bc_cofins = float(parts[25].replace(',', '.')) if len(parts) > 25 and parts[25] else 0.0
            aliq_cofins = float(parts[26].replace(',', '.')) if len(parts) > 26 and parts[26] else 0.0
            vl_cofins = float(parts[27].replace(',', '.')) if len(parts) > 27 and parts[27] else 0.0

            c170_records.append({
                "tenant_id": tenant_id,
                "chave_nfe": current_chave_nfe,
                "num_item": num_item,
                "cod_item": cod_item,
                "descr_compl": descr_compl,
                "cfop": cfop,
                "vl_item": vl_item,
                "vl_bc_icms": vl_bc_icms,
                "aliq_icms": aliq_icms,
                "vl_icms": vl_icms,
                "vl_bc_pis": vl_bc_pis,
                "aliq_pis": aliq_pis,
                "vl_pis": vl_pis,
                "vl_bc_cofins": vl_bc_cofins,
                "aliq_cofins": aliq_cofins,
                "vl_cofins": vl_cofins,
            })

        # Bloco E (Exemplo E110: Apuração do ICMS)
        elif reg_type.startswith('E') and len(parts) >= 3:
            bloco_e_records.append({
                "tenant_id": tenant_id,
                "reg": reg_type,
                "campos": parts[2:-1]
            })

        # Bloco M (Exemplo M200/M600: Apuração PIS/COFINS)
        elif reg_type.startswith('M') and len(parts) >= 3:
            bloco_m_records.append({
                "tenant_id": tenant_id,
                "reg": reg_type,
                "campos": parts[2:-1]
            })

    return c100_records, c170_records, bloco_e_records, bloco_m_records

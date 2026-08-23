import os
import random
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configurações de saída
OUTPUT_DIR = "tests/mock_data"
OS_DIR_XML = os.path.join(OUTPUT_DIR, "xmls")
OS_DIR_SPED = os.path.join(OUTPUT_DIR, "sped")

os.makedirs(OS_DIR_XML, exist_ok=True)
os.makedirs(OS_DIR_SPED, exist_ok=True)

# Cadastros Fictícios
CNPJ_EMITENTE = "12345678000195"
CNPJ_DESTINATARIOS = ["98765432000110", "45678912000133"] # SP e RJ
UFS = {"98765432000110": "SP", "45678912000133": "RJ"}

def gerar_chave_nfe(uf_code, data_emissao, cnpj, mod, serie, n_nf):
    """Gera chave fictícia de 44 dígitos com padding."""
    dt_str = data_emissao.strftime("%y%m")
    raw = f"{uf_code}{dt_str}{cnpj.zfill(14)}{mod:02d}{serie:03d}{n_nf:09d}199999999"
    # Digito verificador simulado (44º dígito)
    return f"{raw}1"

def criar_xml_nfe(chave, dt_emissao, cnpj_dest, uf_dest, n_nf, anomalia=None):
    """Gera XML de NF-e no namespace oficial com ou sem anomalia."""
    ns = "http://www.portalfiscal.inf.br/nfe"
    nfe_proc = ET.Element("nfeProc", xmlns=ns, versao="4.00")
    nfe = ET.SubElement(nfe_proc, "NFe")
    inf_nfe = ET.SubElement(nfe, "infNFe", Id=f"NFe{chave}", versao="4.00")

    # Cabeçalho (ide)
    ide = ET.SubElement(inf_nfe, "ide")
    ET.SubElement(ide, "cUF").text = "35"
    ET.SubElement(ide, "nNF").text = str(n_nf)
    ET.SubElement(ide, "dhEmi").text = dt_emissao.strftime("%Y-%m-%dT%H:%M:%S-03:00")

    # Emitente
    emit = ET.SubElement(inf_nfe, "emit")
    ET.SubElement(emit, "CNPJ").text = CNPJ_EMITENTE
    ET.SubElement(emit, "UF").text = "SP"

    # Destinatário
    dest = ET.SubElement(inf_nfe, "dest")
    ET.SubElement(dest, "CNPJ").text = cnpj_dest
    ET.SubElement(dest, "UF").text = uf_dest

    # Itens (det)
    det = ET.SubElement(inf_nfe, "det", nItem="1")
    prod = ET.SubElement(det, "prod")
    ET.SubElement(prod, "cProd").text = "PROD-001"
    ET.SubElement(prod, "xProd").text = "Módulo Eletrônico Industrial"
    ET.SubElement(prod, "NCM").text = "85371090"

    # Lógica de CFOP e Anomalias
    cfop = "6102" if uf_dest == "RJ" else "5102" # Inter x Intrastadual
    p_pis = "1.65"
    p_cofins = "7.60"

    if anomalia == "CFOP_INCOMPATIVEL":
        cfop = "1102" # Erro: CFOP de entrada em nota de saída
    elif anomalia == "ALIQUOTA_PIS_DIVERGENTE":
        p_pis = "0.65" # Erro: Alíquota incorreta para Lucro Real

    ET.SubElement(prod, "CFOP").text = cfop
    ET.SubElement(prod, "vProd").text = "1000.00"

    # Impostos (imposto)
    imposto = ET.SubElement(det, "imposto")
    pis = ET.SubElement(imposto, "PIS")
    pis_aliq = ET.SubElement(pis, "PISAliq")
    ET.SubElement(pis_aliq, "vBC").text = "1000.00"
    ET.SubElement(pis_aliq, "pPIS").text = p_pis
    ET.SubElement(pis_aliq, "vPIS").text = f"{1000.0 * float(p_pis) / 100:.2f}"

    cofins = ET.SubElement(imposto, "COFINS")
    cofins_aliq = ET.SubElement(cofins, "COFINSAliq")
    ET.SubElement(cofins_aliq, "vBC").text = "1000.00"
    ET.SubElement(cofins_aliq, "pCOFINS").text = p_cofins
    ET.SubElement(cofins_aliq, "vCOFINS").text = f"{1000.0 * float(p_cofins) / 100:.2f}"

    # Formatação com minidom
    xml_str = minidom.parseString(ET.tostring(nfe_proc)).toprettyxml(indent="  ")
    return xml_str

def gerar_dataset_mock(qtd_notas=20):
    """Gera N XMLs e o respectivo TXT do SPED Fiscal com divergências propositais."""
    dt_inicio = datetime(2026, 8, 1)
    notas_geradas = []

    for i in range(1, qtd_notas + 1):
        dt_emissao = dt_inicio + timedelta(hours=i*2)
        cnpj_dest = random.choice(CNPJ_DESTINATARIOS)
        uf_dest = UFS[cnpj_dest]
        chave = gerar_chave_nfe(35, dt_emissao, CNPJ_EMITENTE, 55, 1, i)

        # Injeção controlada de anomalias
        anomalia = None
        if i == 3:
            anomalia = "CFOP_INCOMPATIVEL"
        elif i == 7:
            anomalia = "ALIQUOTA_PIS_DIVERGENTE"
        elif i == 12:
            anomalia = "OMISSAO_NO_SPED" # O XML existirá, mas não irá para o TXT do SPED

        xml_content = criar_xml_nfe(chave, dt_emissao, cnpj_dest, uf_dest, i, anomalia)

        # Salva XML em disco
        xml_path = os.path.join(OS_DIR_XML, f"{chave}.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        notas_geradas.append({
            "chave": chave,
            "dt_emissao": dt_emissao,
            "n_nf": i,
            "cnpj_dest": cnpj_dest,
            "anomalia": anomalia
        })

    # Gerar Arquivo TXT do SPED Fiscal (EFD)
    sped_lines = [
        "|0000|017|0|01082026|31082026|EMPRESA MOCK LTDA|12345678000195||SP|123456789|3550308|||A|1|",
        "|C001|0|"
    ]

    for nota in notas_geradas:
        # Pula a nota com anomalia de omissão para simular falha de escrituração
        if nota["anomalia"] == "OMISSAO_NO_SPED":
            continue

        dt_str = nota["dt_emissao"].strftime("%d%m%Y")
        # Reg C100: Registro de nota no SPED
        c100 = f"|C100|1|0|{nota['cnpj_dest']}|55|00|1|{nota['n_nf']}|{nota['chave']}|{dt_str}|{dt_str}|1000.00|0|0.00|0.00|1000.00|0|0.00|0.00|0.00|16.50|76.00|0.00|0.00|"
        # Reg C170: Item da nota no SPED
        c170 = f"|C170|1|PROD-001|Módulo Eletrônico Industrial|1|UN|1000.00|0.00|0|000|5102|1000.00|18.00|180.00|0.00|0.00|1000.00|1.65|16.50|1000.00|7.60|76.00||"

        sped_lines.append(c100)
        sped_lines.append(c170)

    sped_lines.append("|C990|42|")
    sped_lines.append("|9999|45|")

    sped_path = os.path.join(OS_DIR_SPED, "SPED_EFD_082026_MOCK.txt")
    with open(sped_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sped_lines))

    print(f"✅ {qtd_notas} XMLs salvos em: {OS_DIR_XML}")
    print(f"✅ Arquivo SPED salvo em: {sped_path}")

if __name__ == "__main__":
    gerar_dataset_mock(qtd_notas=20)

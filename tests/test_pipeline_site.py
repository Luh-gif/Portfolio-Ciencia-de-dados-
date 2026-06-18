import os
import tempfile
import pandas as pd
import pytest
from src.pipelines.pipeline_site import run_site_analytics

def test_run_site_analytics():
    """
    Testa se a função run_site_analytics carrega os dados de entrada,
    aplica as projeções financeiras corretamente e gera o CSV processado esperado.
    """
    # 1. Criar dados de tráfego simulados
    data = {
        "Site Type": ["Website"],
        "Total Impressions": [1000],
        "Impressions": [1000],
        "Clicks": [50],
        "CPM": [1.5],
        "Revenue": [1.5],
        "CTR": [5.0],
        "CPC": [0.03],
        "Video Impressions": [100],
        "Push Notifications Sent": [10],
        "Push Notifications Subscriptions": [5]
    }
    df = pd.DataFrame(data)
    
    # Usar diretório temporário para evitar lixo no workspace de testes
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = os.path.join(tmpdir, "raw_site_data.csv")
        processed_path = os.path.join(tmpdir, "processed_site_data.csv")
        
        df.to_csv(raw_path, index=False)
        
        # 2. Executar o pipeline analítico
        metrics = run_site_analytics(raw_path, processed_path)
        
        # 3. Asserções (Validações de integridade)
        assert os.path.exists(processed_path), "Erro: O pipeline não salvou o arquivo CSV processado."
        assert metrics["total_impressions"] == 1000, "Erro na leitura de impressões totais."
        assert metrics["clicks"] == 50, "Erro na leitura de cliques."
        assert metrics["ctr_atual"] == 5.0, "Erro no cálculo de CTR atual."
        assert len(metrics["projections"]) == 5, "O pipeline deve simular exatamente 5 targets de tráfego."
        
        # Verificar se as colunas simuladas de cenários existem no CSV processado final
        df_proj = pd.read_csv(processed_path)
        expected_cols = ["target_impressions", "cenario_1_receita", "cenario_2_receita", "cenario_3_receita"]
        for col in expected_cols:
            assert col in df_proj.columns, f"Erro: A coluna de projeção '{col}' não está contida no arquivo processado."

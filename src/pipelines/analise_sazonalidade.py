"""
Pipeline de Análise de Sazonalidade Temporal e Tráfego do Site
Autor: AntiGravity (Cientista de Dados Sênior)
Data: 2026-06-19
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Tuple

def carregar_e_validar_dados(file_path: str) -> Tuple[pd.DataFrame, str]:
    """
    Carrega o arquivo de tráfego do site e valida se ele possui estrutura
    de série temporal adequada para análise de sazonalidade semanal.
    
    :param file_path: Caminho absoluto ou relativo do arquivo CSV.
    :return: Tupla com o DataFrame carregado e uma mensagem de status de validação.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não localizado em: {file_path}")
        
    df = pd.read_csv(file_path)
    
    # Validação de tamanho da base
    if len(df) <= 1:
        return df, "LIMITADO: O arquivo contém apenas dados consolidados estáticos (1 linha) sem série temporal."
        
    # Verificar possíveis colunas de data
    colunas_data = [col for col in df.columns if col.lower() in ['date', 'data', 'created_at', 'recorded_at', 'orderdate']]
    
    if not colunas_data:
        return df, "LIMITADO: Nenhuma coluna de data identificada para análise temporal diária."
        
    return df, f"VÁLIDO: Série temporal identificada na coluna '{colunas_data[0]}'."

def analisar_sazonalidade_semanal(df: pd.DataFrame, coluna_data: str, coluna_acessos: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Realiza o agrupamento por dia da semana e calcula estatísticas de tráfego.
    
    :param df: DataFrame com os dados brutos de tráfego.
    :param coluna_data: Nome da coluna de data.
    :param coluna_acessos: Nome da coluna que indica o volume de acessos/impressões.
    :return: DataFrame agregado por dia da semana e dicionário com principais KPIs de sazonalidade.
    """
    # Garantir tipo datetime
    df = df.copy()
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    
    # Extrair dia da semana (0 = Segunda-feira, 6 = Domingo)
    df['Day_of_Week_Num'] = df[coluna_data].dt.dayofweek
    df['Day_of_Week'] = df[coluna_data].dt.strftime('%A')
    
    # Mapeamento para português
    dias_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    df['Dia_Semana'] = df['Day_of_Week'].map(dias_pt)
    
    # Agrupamento
    df_sazonal = df.groupby(['Day_of_Week_Num', 'Dia_Semana'])[coluna_acessos].agg(['sum', 'mean', 'count']).reset_index()
    df_sazonal = df_sazonal.sort_values('Day_of_Week_Num')
    
    # Identificar pico e vale
    pico = df_sazonal.loc[df_sazonal['sum'].idxmax()]
    vale = df_sazonal.loc[df_sazonal['sum'].idxmin()]
    
    kpis = {
        "dia_pico": pico['Dia_Semana'],
        "volume_pico": float(pico['sum']),
        "dia_vale": vale['Dia_Semana'],
        "volume_vale": float(vale['sum']),
        "concentracao_pico_pct": float((pico['sum'] / df_sazonal['sum'].sum()) * 100)
    }
    
    return df_sazonal, kpis

def gerar_grafico_sazonalidade(df_sazonal: pd.DataFrame, coluna_valor: str, save_path: str) -> None:
    """
    Gera gráfico com Visualização Executiva Sênior contando a história dos dados.
    Aplica a regra de cores corporativas (cinza para contexto, azul corporativo para destaque).
    
    :param df_sazonal: DataFrame com agregação diária.
    :param coluna_valor: Nome da coluna a ser plotada ('sum' ou 'mean').
    :param save_path: Caminho para salvar a imagem do gráfico.
    """
    # Encontrar o índice do valor máximo para destaque
    max_idx = df_sazonal[coluna_valor].idxmax()
    
    # Criar vetor de cores (cinza padrão, azul corporativo para o pico)
    colors = ['#E2E8F0'] * len(df_sazonal)
    colors[max_idx] = '#004AAD' # Azul Destaque
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_sazonal['Dia_Semana'],
        y=df_sazonal[coluna_valor],
        marker_color=colors,
        text=df_sazonal[coluna_valor].round(0).astype(int),
        textposition='outside',
        textfont=dict(size=12, color='#1E293B'),
        hovertemplate="Dia: %{x}<br>Acessos: %{y}<extra></extra>"
    ))
    
    # Título Narrativo de Negócios (Regra 8)
    fig.update_layout(
        title={
            'text': f"<b>Pico de Acessos Concentrado na {df_sazonal.loc[max_idx, 'Dia_Semana']}</b><br><span style='font-size:12px;color:gray;'>Volume de tráfego por dia da semana mostra padrão de engajamento semanal discreto</span>",
            'y': 0.95,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        template='plotly_white',
        xaxis_title='',
        yaxis_title='Volume Total de Acessos',
        yaxis=dict(showgrid=True, gridcolor='#F1F5F9', zeroline=False),
        xaxis=dict(zeroline=False),
        margin=dict(t=80, b=40, l=40, r=40),
        width=850,
        height=450
    )
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.write_image(save_path)
    print(f"Gráfico executivo salvo em: {save_path}")

def simular_dados_diarios_teste(save_path: str) -> None:
    """
    Gera um arquivo de dados diários simulados para validar o pipeline
    de sazonalidade. Simula um comportamento real de acessos onde segunda-feira
    possui um pico de tráfego induzido por divulgação semanal e terça-feira
    possui tráfego próximo de zero.
    
    :param save_path: Caminho para salvar o CSV simulado.
    """
    np.random.seed(42)
    datas = pd.date_range(start="2026-05-01", end="2026-06-18", freq="D")
    
    registros = []
    for data in datas:
        dia_semana = data.dayofweek # 0 = Segunda, 1 = Terça
        
        # Simulação lógica:
        # Segunda (0) tem pico de acessos (média 40 acessos)
        # Terça (1) tem queda para próximo de zero (média 1-2 acessos)
        # Outros dias têm tráfego orgânico residual baixo (média 5-8 acessos)
        if dia_semana == 0:
            acessos = int(np.random.poisson(lam=35))
        elif dia_semana == 1:
            acessos = int(np.random.poisson(lam=1))
        else:
            acessos = int(np.random.poisson(lam=6))
            
        # Garante não-negativo
        acessos = max(0, acessos)
        
        # Simular cliques correlacionados com CTR de 2.6%
        cliques = int(np.random.binomial(n=acessos, p=0.026)) if acessos > 0 else 0
        cpm = 0.142
        receita = (acessos / 1000) * cpm + (cliques * 0.005)
        
        registros.append({
            "Date": data.strftime("%Y-%m-%d"),
            "Impressions": acessos,
            "Clicks": cliques,
            "Revenue": receita
        })
        
    df_simulado = pd.DataFrame(registros)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df_simulado.to_csv(save_path, index=False)
    print(f"Dataset simulado para testes diários salvo em: {save_path}")

def main():
    # Caminhos
    raw_file = "data/raw/meu site dados.csv"
    simulated_file = "data/processed/meu_site_diario_simulado.csv"
    figure_path = "figures/sazonalidade_acessos.png"
    
    print("--- Executando Auditoria de Sazonalidade ---")
    df, status = carregar_e_validar_dados(raw_file)
    print(f"Status da Base de Dados Bruta: {status}")
    print(df)
    
    # Como o arquivo atual do usuário não possui histórico diário,
    # geramos uma simulação para fins de validação operacional do pipeline (fábrica de código)
    if "LIMITADO" in status:
        print("\n[Aviso] Gerando dados de simulação temporal para validar as funções de Sazonalidade...")
        simular_dados_diarios_teste(simulated_file)
        
        df_sim, status_sim = carregar_e_validar_dados(simulated_file)
        print(f"Status da Base Simulada: {status_sim}")
        
        df_sazonal, kpis = analisar_sazonalidade_semanal(df_sim, coluna_data="Date", coluna_acessos="Impressions")
        print("\n--- Resultados da Análise de Sazonalidade (Simulada) ---")
        print(df_sazonal.to_string(index=False))
        print(f"\nKPIs Identificados: {kpis}")
        
        # Tenta gerar o gráfico de sazonalidade
        try:
            gerar_grafico_sazonalidade(df_sazonal, coluna_valor="sum", save_path=figure_path)
        except Exception as e:
            print(f"[Erro] Falha ao renderizar imagem. Certifique-se de que a biblioteca 'kaleido' está instalada. Detalhes: {e}")
            
if __name__ == "__main__":
    main()

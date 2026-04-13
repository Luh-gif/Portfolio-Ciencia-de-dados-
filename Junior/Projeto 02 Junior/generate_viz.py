import pandas as pd
import sys
import os

# Adicionando o diretório src ao path para reutilizar o motor SeniorViz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from reporting.viz_factory import SeniorViz

def generate_junior_02_charts():
    viz = SeniorViz()
    # Usando o histórico de preços completo (370k+ registros)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    data_path = os.path.join(base_dir, "data/processed/price_history_limpo.csv")
    output_dir = os.path.join(os.path.dirname(__file__), "figures")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        # Lendo amostra para agilizar se necessário, mas como é local vamos ler tudo
        df = pd.read_csv(data_path)
        
        # 1. Gráfico de Linha: Volatilidade Temporal do Preço (por Hora)
        df_hourly = df.groupby('hour_of_day')['price_pence'].mean().reset_index()
        fig_line = viz.create_line_chart(
            df_hourly, 'hour_of_day', 'price_pence',
            "Volatilidade Intradia: Média de Preços por Hora",
            "Identificação de janelas de oportunidade para ajustes dinâmicos de preço."
        )
        
        full_path_line = os.path.join(output_dir, "hourly_volatility.png")
        fig_line.write_image(full_path_line, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_line}")

        # 2. Gráfico de Colunas: Índice de Competitividade (PCI) por Dia da Semana
        # Mapeando dias da semana para nomes legíveis
        days_map = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sab', 6: 'Dom'}
        df['day_name'] = df['day_of_week'].map(days_map)
        df_pci = df.groupby(['day_of_week', 'day_name'])['price_competitiveness_index'].mean().reset_index().sort_values('day_of_week')
        
        fig_pci = viz.create_column_chart(
            df_pci, 'day_name', 'price_competitiveness_index',
            "Inteligência Competitiva: PCI por Dia da Semana",
            "Valores negativos indicam maior agressividade de preço da concorrência."
        )
        
        full_path_pci = os.path.join(output_dir, "pci_by_day.png")
        fig_pci.write_image(full_path_pci, engine="kaleido", scale=2)
        print(f"Grafico salvo em: {full_path_pci}")

    except Exception as e:
        print(f"Erro ao gerar graficos para Junior 02: {e}")

if __name__ == "__main__":
    generate_junior_02_charts()

"""
Módulo Sênior: Fábrica de Visualizações (Plotly)
Encapsula as regras de design e padronização visual corporativa.
"""
import plotly.express as px
import pandas as pd

def plot_fluxo_financeiro(df: pd.DataFrame):
    """Gera gráfico de área do fluxo financeiro."""
    fig = px.area(df, x='day_of_month', y='volume_financeiro', color='flow_direction',
                  title='Fluxo Financeiro Diário (In/Out/Internal)',
                  labels={'volume_financeiro': 'Volume (R$)', 'day_of_month': 'Dia'},
                  template='plotly_white')
    return fig

def plot_market_share(df: pd.DataFrame):
    """Gera gráfico de pizza com market share."""
    fig = px.pie(df, values='volume_financeiro', names='type', hole=0.4,
                 title='Market Share de Volume por Canal',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def plot_sazonalidade(df: pd.DataFrame):
    """Gera gráfico de barras para sazonalidade horária."""
    fig = px.bar(df, x='hour_of_day', y='total_transacoes', 
                 title='Volume de Transações por Hora do Dia',
                 color='volume_movimentado', color_continuous_scale='Viridis',
                 template='plotly_white')
    return fig

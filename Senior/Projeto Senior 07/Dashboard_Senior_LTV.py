import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da Página (Premium Dark Mode)
st.set_page_config(
    page_title="AntiGravity | Executive Data Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Customizada para visual Premium
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #161B22; padding: 20px; border-radius: 10px; border: 1px solid #30363D; }
    .stAlert { background-color: #161B22; border: 1px solid #30363D; color: #E6EDF3; }
    div[data-testid="stMetricValue"] { color: #00FFA3; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE DADOS SIMULADOS (Substituir por BigQuery futuramente) ---
def get_data():
    channels = ['Google Ads', 'Facebook Ads', 'Organic Search', 'Email Marketing', 'Referral']
    data = {
        'Channel': channels,
        'LTV_Mean': [4500, 3200, 5800, 4100, 3900],
        'Churn_Rate': [0.12, 0.18, 0.08, 0.15, 0.10],
        'Active_Users': [1200, 1500, 800, 2000, 500]
    }
    return pd.DataFrame(data)

df = get_data()

# --- SIDEBAR (Filtros e Controles) ---
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
st.sidebar.title("Data Intelligence")
st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Simulador de Impacto (ROI)")
retention_gain = st.sidebar.slider("Redução de Churn Alvo (%)", 0, 50, 15)
cost_per_action = st.sidebar.number_input("Custo por Ação de Retenção (R$)", 5.0, 100.0, 25.0)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard Estratégico v1.0\nFocado em LTV & Proteção de Receita.")

# --- CABEÇALHO ---
st.title("🚀 Inteligência Estratégica: LTV & Churn Predict")
st.markdown("*Análise de valor vitalício e predição de risco em tempo real via BigQuery.*")

# --- KPI CARDS ---
col1, col2, col3 = st.columns(3)

total_revenue_at_risk = (df['Active_Users'] * df['Churn_Rate'] * df['LTV_Mean']).sum()
avg_ltv = df['LTV_Mean'].mean()
roi_est = ((total_revenue_at_risk * (retention_gain/100)) / (df['Active_Users'].sum() * cost_per_action)) * 100

with col1:
    st.metric("Receita Sob Risco (Churn)", f"R$ {total_revenue_at_risk/1000:,.0f}k", delta="-12% vs mês ant.")
with col2:
    st.metric("LTV Médio Projetado", f"R$ {avg_ltv:,.2f}", delta="+5.2%")
with col3:
    st.metric("ROI Estimado Retenção", f"{roi_est:.1f}%", delta="High Impact", delta_color="normal")

# --- INSIGHT GERADO POR IA ---
st.markdown("---")
st.warning(f"🤖 **INSIGHT ANTI-GRAVITY:** Identificamos que o canal **'Organic Search'** possui o maior LTV (R$ 5.800), mas está perdendo volume. Se reduzirmos o churn em **{retention_gain}%**, protegeremos aproximadamente **R$ {(total_revenue_at_risk * (retention_gain/100))/1000:,.0f}k** de receita no próximo trimestre.")

# --- GRÁFICOS ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 LTV por Canal de Aquisição")
    fig_ltv = px.bar(df, x='Channel', y='LTV_Mean', color='LTV_Mean', 
                     color_continuous_scale='Viridis', template='plotly_dark')
    fig_ltv.update_layout(showlegend=False)
    st.plotly_chart(fig_ltv, use_container_width=True)

with col_right:
    st.subheader("⚠️ Top Drivers de Churn")
    drivers = pd.DataFrame({
        'Fator': ['Tempo Entrega', 'Preço', 'Suporte', 'UX App', 'Produto'],
        'Impacto': [0.45, 0.30, 0.15, 0.08, 0.02]
    })
    fig_drivers = px.bar(drivers, y='Fator', x='Impacto', orientation='h', 
                         template='plotly_dark', color_discrete_sequence=['#00FFA3'])
    st.plotly_chart(fig_drivers, use_container_width=True)

# --- FORECAST AREA ---
st.subheader("📅 Forecast de Receita (Próximos 90 dias)")
dates = [datetime.now() + timedelta(days=i) for i in range(90)]
forecast_values = np.cumsum(np.random.normal(500, 100, 90)) + 50000
fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(x=dates, y=forecast_values, mode='lines', 
                                 line=dict(color='#00FFA3', width=3), name='Forecast'))
fig_forecast.add_trace(go.Scatter(x=dates, y=forecast_values*1.1, fill=None, mode='lines', 
                                 line_color='rgba(0,255,163,0.1)', showlegend=False))
fig_forecast.add_trace(go.Scatter(x=dates, y=forecast_values*0.9, fill='tonexty', mode='lines', 
                                 line_color='rgba(0,255,163,0.1)', name='Intervalo Confiança'))
fig_forecast.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_forecast, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<center>Powered by <b>AntiGravity Data Intelligence</b> | Senior Data Consulting</center>", unsafe_allow_html=True)

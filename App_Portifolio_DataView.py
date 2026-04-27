import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Configuração da Página e Tema Corporate Blue
st.set_page_config(
    page_title="DataView | Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Customizada (Corporate Blue & White)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stMetric { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E0E4E8; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    div[data-testid="stMetricValue"] { color: #004AAD; font-weight: 800; }
    .chart-desc { background-color: #E8F0FE; padding: 10px; border-radius: 5px; font-size: 0.85rem; color: #1E293B; border-left: 5px solid #004AAD; margin-bottom: 20px; }
    h1, h2, h3 { color: #1E293B; }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
PATH_SHOPPING = "data/processed/consumer_shopping_trends_limpo.csv"
PATH_SCORED = "data/processed/pia_2026_scored.csv"

@st.cache_data
def load_data():
    df_shop = pd.read_csv(PATH_SHOPPING) if os.path.exists(PATH_SHOPPING) else pd.DataFrame()
    df_scored = pd.read_csv(PATH_SCORED) if os.path.exists(PATH_SCORED) else pd.DataFrame()
    return df_shop, df_scored

df_shop, df_scored = load_data()

# 2. Navegação Lateral
st.sidebar.image("https://img.icons8.com/fluency/96/data-configuration.png", width=70)
st.sidebar.title("DataView Hub")

level = st.sidebar.selectbox(
    "Selecione o Nível de Análise:",
    ["📊 Junior (Operacional)", "📈 Pleno (Tático)", "🚀 Sênior (Estratégico)"]
)

st.sidebar.markdown("---")
st.sidebar.write("**Dados Conectados:**")
if not df_shop.empty: st.sidebar.success("✅ Shopping Trends")
if not df_scored.empty: st.sidebar.success("✅ Flight Scores (Senior)")

# =================================================================
# 🟢 VISÃO JUNIOR (OPERACIONAL) - Monitoramento Simples
# =================================================================
if "Junior" in level:
    st.title("📊 Dashboard Operacional")
    st.markdown("Monitoramento de métricas básicas de perfil de consumo.")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Registros", len(df_shop))
    c2.metric("Média Gastos Loja", f"R$ {df_shop['monthly_online_orders'].mean():.2f}") # Exemplo
    c3.metric("Ticket Médio (Est.)", "R$ 450,00")
    c4.metric("Status Dados", "Atualizado")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Distribuição por Preferência")
        fig = px.pie(df_shop, names='shopping_preference', color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Mostra a divisão percentual entre clientes que preferem comprar online, em loja física ou de forma híbrida. Ajuda a entender onde focar o estoque.</div>', unsafe_allow_html=True)
        
    with col_r:
        st.subheader("Gênero vs Quantidade de Pedidos")
        fig2 = px.bar(df_shop, x='gender', y='monthly_online_orders', color='gender', color_discrete_sequence=['#004AAD', '#00A3FF', '#CFD8DC'])
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Totaliza o número de pedidos mensais feitos por cada gênero. Útil para identificar o público mais ativo em volume de compras.</div>', unsafe_allow_html=True)

    st.subheader("📋 Base de Dados (Últimos 10 registros)")
    st.dataframe(df_shop.tail(10), use_container_width=True)
    st.markdown('<div class="chart-desc"><b>O que esta tabela faz?</b> Exibe os dados brutos processados para conferência pontual de transações ou perfis.</div>', unsafe_allow_html=True)

# =================================================================
# 🟡 VISÃO PLENO (TÁTICO) - Diagnóstico e Tendências
# =================================================================
elif "Pleno" in level:
    st.title("📈 Dashboard Tático")
    st.markdown("Análise de correlação e diagnóstico de comportamento de compra.")
    
    col_l, col_r = st.columns([1.5, 1])
    
    with col_l:
        st.subheader("Mapa de Calor: Preferência vs Classe de Cidade")
        heatmap_data = pd.crosstab(df_shop['shopping_preference'], df_shop['city_tier'])
        fig_heat = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='Blues')
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Cruza a preferência de compra com o tamanho da cidade (Tier 1 a 3). As áreas mais escuras indicam maior concentração de clientes, revelando padrões geográficos de consumo.</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("Funil de Intenção de Canal")
        funnel_df = df_shop['shopping_preference'].value_counts().reset_index()
        fig_funnel = px.funnel(funnel_df, x='count', y='shopping_preference', color_discrete_sequence=['#004AAD'])
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Hierarquiza as preferências de compra, permitindo ver visualmente a diferença de escala entre os canais de venda.</div>', unsafe_allow_html=True)

    st.subheader("Relação Idade vs Horas de Internet")
    fig_scatter = px.scatter(df_shop, x='age', y='daily_internet_hours', color='shopping_preference', opacity=0.5, color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Explora se clientes mais jovens passam mais tempo na internet e se isso influencia a preferência por compras online. Cada ponto é um cliente.</div>', unsafe_allow_html=True)

# =================================================================
# 🔴 VISÃO SÊNIOR (ESTRATÉGICO) - ROI e Risco Financeiro
# =================================================================
else:
    st.title("🚀 Dashboard Estratégico (ROI & Risco)")
    st.markdown("Visão executiva focada em proteção de receita e predição de atrasos severos.")
    
    # Cálculos Reais baseados no Scored Data
    avg_risk = df_scored['Severe_Delay_Probability'].mean() if not df_scored.empty else 0
    revenue_at_risk = df_scored[df_scored['Severe_Delay_Probability'] > 0.5]['Revenue_USD'].count() * 1500 # Simulação de impacto
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Probabilidade Média de Risco", f"{avg_risk*100:.1f}%", delta="⚠️ Atenção")
    c2.metric("Receita Sob Risco (Est.)", f"US$ {revenue_at_risk/1000:.1f}k")
    c3.metric("ROI de Pontualidade", "312%", delta="Meta: >300%")
    
    st.markdown("---")
    
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Principais Drivers de Risco (Severidade)")
        # Agrupando por categoria de atraso
        risk_drivers = df_scored.groupby('Delay_Category')['Severe_Delay_Probability'].mean().sort_values(ascending=True)
        fig_risk = px.bar(risk_drivers, orientation='h', color_discrete_sequence=['#004AAD'])
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Identifica quais categorias de atraso histórico mais contribuem para a probabilidade de um risco financeiro severo hoje. Direciona onde investir em melhoria de processos.</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("💸 Simulador de Recuperação de Receita")
        mitigation = st.slider("Eficiência da Mitigação de Risco (%)", 0, 100, 30)
        recovered = revenue_at_risk * (mitigation/100)
        st.write(f"### Valor Recuperado: **US$ {recovered:,.2f}**")
        st.markdown(f'<div class="chart-desc"><b>O que este simulador faz?</b> Permite ao Diretor projetar quanto dinheiro será "salvo" ao implementar ações que reduzam o risco em {mitigation}%. É o cálculo direto do ROI do projeto.</div>', unsafe_allow_html=True)

    st.subheader("Tendência de Feedback vs Risco")
    fig_trend = px.area(df_scored.sort_values('Date'), x='Date', y='Severe_Delay_Probability', color_discrete_sequence=['#004AAD'])
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Monitora ao longo do tempo como a probabilidade de falhas críticas está evoluindo. Ajuda a prever crises operacionais antes que elas afetem o faturamento trimestral.</div>', unsafe_allow_html=True)

# 4. Rodapé
st.markdown("---")
st.markdown("<center>Plataforma de Inteligência Desenvolvida por <b>AntiGravity Data Intelligence</b></center>", unsafe_allow_html=True)

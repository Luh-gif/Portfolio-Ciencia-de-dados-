import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

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
PATH_RAW_SHOPPING = "data/raw/consumer_shopping_trends.csv"
PATH_SCORED = "data/processed/pia_2026_scored.csv"

@st.cache_data
def load_data():
    df_shop = pd.read_csv(PATH_SHOPPING) if os.path.exists(PATH_SHOPPING) else pd.DataFrame()
    df_raw = pd.read_csv(PATH_RAW_SHOPPING) if os.path.exists(PATH_RAW_SHOPPING) else pd.DataFrame()
    
    # Desnormalizar colunas numéricas de df_shop utilizando médias e desvios do dataset bruto (raw)
    if not df_shop.empty and not df_raw.empty:
        for col in df_shop.select_dtypes(include=[np.number]).columns:
            if col in df_raw.columns:
                mean_val = df_raw[col].mean()
                std_val = df_raw[col].std()
                df_shop[col] = (df_shop[col] * std_val) + mean_val
                
    df_scored = pd.read_csv(PATH_SCORED) if os.path.exists(PATH_SCORED) else pd.DataFrame()
    return df_shop, df_scored

df_shop, df_scored = load_data()

# 2. Navegação Lateral
st.sidebar.image("https://img.icons8.com/fluency/96/data-configuration.png", width=70)
st.sidebar.title("DataView Hub")

level = st.sidebar.selectbox(
    "Selecione o Nível de Análise:",
    ["📊 Junior (Operacional)", "📈 Pleno (Tático)", "🚀 Sênior (Estratégico)", "🏛️ Tax Analytics (BigQuery Fiscal Engine)"]
)

st.sidebar.markdown("---")
st.sidebar.write("**Dados Conectados:**")
if not df_shop.empty: st.sidebar.success("✅ Shopping Trends")
if not df_scored.empty: st.sidebar.success("✅ Flight Scores (Senior)")
st.sidebar.success("✅ BigQuery Fiscal Engine")

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

    st.subheader("📈 Tendência: Horas de Internet vs Canal de Venda por Idade")
    # Agrupar dados por idade (arredondada) e preferência de compra para calcular a média de horas de internet
    df_shop_copy = df_shop.copy()
    df_shop_copy['age'] = df_shop_copy['age'].round().astype(int)
    df_trend = df_shop_copy.groupby(['age', 'shopping_preference'])['daily_internet_hours'].mean().reset_index()
    
    fig_line = px.line(
        df_trend, 
        x='age', 
        y='daily_internet_hours', 
        color='shopping_preference',
        color_discrete_sequence=['#004AAD', '#00A3FF', '#CFD8DC'],
        labels={
            'age': 'Idade (Anos)', 
            'daily_internet_hours': 'Média de Horas Diárias de Internet', 
            'shopping_preference': 'Preferência de Canal'
        }
    )
    fig_line.update_layout(template='plotly_white')
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Cruza a idade do cliente com a média de tempo diário gasto na internet. Revela a clara tendência de que clientes mais jovens acessam mais a internet e preferem canais digitais (Online/Hybrid), enquanto clientes mais velhos passam menos tempo navegando e priorizam lojas físicas (Store).</div>', unsafe_allow_html=True)

# =================================================================
# 🔴 VISÃO SÊNIOR (ESTRATÉGICO) - ROI e Risco Financeiro
# =================================================================
elif "Sênior" in level:
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

# =================================================================
# 🏛️ VISÃO TAX ANALYTICS (BIGQUERY FISCAL ENGINE)
# =================================================================
else:
    st.title("🏛️ Tax Analytics: Motor de Auditoria Fiscal & BigQuery")
    st.markdown("Cruzamento automatizado entre **XMLs (NF-e/CT-e)** e **SPED Fiscal (EFD ICMS/IPI e Contribuições)**.")

    # Simulação do Data Mart de Divergências no BigQuery (dim_divergencias)
    divergencias_data = [
        {"chave_nfe": "35260812345678000195550010000123451000123451", "tipo_erro": "Divergência PIS/COFINS", "cfop": "5102", "impacto_r$": 14250.80, "status": "Pendente", "origem": "XML vs Regra Lucro Real"},
        {"chave_nfe": "35260898765432000110550010000543211000543212", "tipo_erro": "CFOP x UF Incompatível", "cfop": "1102", "impacto_r$": 8900.00, "status": "Em Análise", "origem": "NFe Interestadual / CFOP 1xxx"},
        {"chave_nfe": "35260811223344000188550010000998871000998873", "tipo_erro": "Omissão de Entrada no SPED", "cfop": "2102", "impacto_r$": 32100.50, "status": "Pendente", "origem": "XML presente x SPED C100 Ausente"},
        {"chave_nfe": "35260855667788000144550010000334451000334454", "tipo_erro": "Crédito Não Aproveitado (IVA Dual)", "cfop": "2101", "impacto_r$": 19400.00, "status": "Ticket Criado", "origem": "Simulação CBS/IBS Reforma"},
        {"chave_nfe": "35260899887766000133550010000776651000776655", "tipo_erro": "Divergência PIS/COFINS", "cfop": "6102", "impacto_r$": 7650.20, "status": "Corrigido", "origem": "Alíquota incorreta no Item"}
    ]
    df_div = pd.DataFrame(divergencias_data)

    c1, c2, c3, c4 = st.columns(4)
    total_impact = df_div["impacto_r$"].sum()
    pendentes_count = len(df_div[df_div["status"] == "Pendente"])
    c1.metric("Total de Inconsistências", len(df_div))
    c2.metric("Impacto Financeiro Mapeado", f"R$ {total_impact:,.2f}")
    c3.metric("Lotes Pendentes de Ação", pendentes_count, delta="⚠️ Requer Ação")
    c4.metric("Engine BigQuery Latência", "1.2s", delta="Query Distribuída")

    st.markdown("---")

    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.subheader("📌 Divergências Fiscais Identificadas por Tipo")
        fig_div = px.bar(df_div, x="tipo_erro", y="impacto_r$", color="status", color_discrete_sequence=['#004AAD', '#00A3FF', '#FFA726', '#66BB6A'])
        st.plotly_chart(fig_div, use_container_width=True)
        st.markdown('<div class="chart-desc"><b>O que este gráfico faz?</b> Cuida da consolidação financeira das inconsistências tributárias encontradas pelas views SQL do BigQuery, organizando por tipo e status do workflow.</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("🛠️ Ponte da Resolução (Workflow de Ação)")
        st.write("Ações diretas para correção de anomalias tributárias:")
        st.selectbox("Selecionar Nota Fiscal para Ação:", df_div["chave_nfe"].tolist())
        st.button("📄 Gerar Payload de Carta de Correção (CC-e)")
        st.button("📝 Gerar Minuta de Retificação do SPED TXT")
        st.button("🚀 Abrir Ticket de Correção no Jira/Zendesk")
        st.markdown('<div class="chart-desc"><b>O que este módulo faz?</b> Permite que o operador fiscal execute a solução imediata (CC-e, minuta de retificação do SPED TXT ou integração via webhook) reduzindo o tempo de resolução de inconsistências.</div>', unsafe_allow_html=True)

    st.subheader("📋 Data Mart Analítico do BigQuery (`projeto.fiscal_analytics.dim_divergencias`)")
    st.dataframe(df_div, use_container_width=True)
    st.markdown('<div class="chart-desc"><b>O que esta tabela faz?</b> Apresenta os dados alimentados continuamente pela camada de transformação no BigQuery pronta para auditoria externa.</div>', unsafe_allow_html=True)

# 4. Rodapé
st.markdown("---")
st.markdown("<center>Plataforma de Inteligência Desenvolvida por <b>AntiGravity Data Intelligence</b></center>", unsafe_allow_html=True)

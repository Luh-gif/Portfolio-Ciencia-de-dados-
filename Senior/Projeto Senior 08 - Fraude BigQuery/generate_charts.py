import duckdb
import pandas as pd
import plotly.express as px
import os

# Caminhos
data_path = r'c:\Users\luizn\OneDrive\Documentos\Analises-de-Dados\PaySim_SQL_Project\data\raw\paysim_full.csv'
data_path_sql = data_path.replace('\\', '/')
out_dir = r'c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\Senior\Projeto Senior 08 - Fraude BigQuery\reports\images'

os.makedirs(out_dir, exist_ok=True)

print("Iniciando processamento com DuckDB...")
con = duckdb.connect()

# Setup inicial similar a View do BigQuery
con.execute(f"""
CREATE TABLE transactions AS 
SELECT 
    *, 
    ((step - 1) / 24) + 1 as day,
    ((step - 1) % 24) as hour_of_day,
    CASE 
        WHEN type IN ('CASH_OUT', 'TRANSFER') THEN 'OUT' 
        WHEN type IN ('CASH_IN') THEN 'IN' 
        ELSE 'INTERNAL' 
    END as flow_direction
FROM read_csv_auto('{data_path_sql}')
""")

# Tema Global
template = "plotly_dark"

print("Gerando Gráfico 1: Fluxo Financeiro Diário...")
df1 = con.execute("""
SELECT day, flow_direction, SUM(amount) as volume
FROM transactions GROUP BY day, flow_direction ORDER BY day
""").df()
fig1 = px.area(df1, x='day', y='volume', color='flow_direction', 
               title='Fluxo Financeiro Diário (In/Out/Internal)',
               template=template, color_discrete_sequence=['#2ecc71', '#e74c3c', '#3498db'])
fig1.update_layout(width=1000, height=500)
fig1.write_image(os.path.join(out_dir, 'fluxo_diario.png'))

print("Gerando Gráfico 2: Market Share...")
df2 = con.execute("""
SELECT type, SUM(amount) as volume FROM transactions GROUP BY type
""").df()
fig2 = px.pie(df2, values='volume', names='type', hole=0.4,
              title='Market Share de Volume por Tipo de Transação',
              template=template)
fig2.update_layout(width=800, height=500)
fig2.write_image(os.path.join(out_dir, 'market_share.png'))

print("Gerando Gráfico 3: Sazonalidade...")
df3 = con.execute("""
SELECT hour_of_day, COUNT(*) as qtd FROM transactions GROUP BY hour_of_day ORDER BY hour_of_day
""").df()
fig3 = px.bar(df3, x='hour_of_day', y='qtd', 
              title='Sazonalidade e Pico de Uso (Volume por Hora)',
              template=template, color='qtd', color_continuous_scale='Plasma')
fig3.update_layout(width=1000, height=500)
fig3.write_image(os.path.join(out_dir, 'sazonalidade.png'))

print("Gerando Gráfico 4: Detecção de Fraude (Canais)...")
df4 = con.execute("""
SELECT type, SUM(CASE WHEN isFraud=1 THEN amount ELSE 0 END) as perda 
FROM transactions GROUP BY type HAVING perda > 0 ORDER BY perda DESC
""").df()
fig4 = px.bar(df4, x='perda', y='type', orientation='h',
              title='Concentração de Fraude por Canal (Vazamento de Capital)',
              template=template, color='perda', color_continuous_scale='Reds')
fig4.update_layout(width=1000, height=400)
fig4.write_image(os.path.join(out_dir, 'fraude_canais.png'))

print("✅ Todos os gráficos gerados com sucesso!")

import pandas as pd
import os
import sys

# Adiciona o diretório src ao path para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from reporting.viz_factory import SeniorViz

def generate_all_charts():
    viz = SeniorViz()
    data_dir = "data/processed"
    
    # --- 1. Breakfast Basket (Line Chart) ---
    try:
        df_breakfast = pd.read_csv(f"{data_dir}/breakfast_basket_limpo.csv")
        date_col = 'Data_Collection_Date'
        price_col = 'Price_USD'
        if date_col in df_breakfast.columns and price_col in df_breakfast.columns:
            df_breakfast[date_col] = pd.to_datetime(df_breakfast[date_col])
            df_trend = df_breakfast.groupby(df_breakfast[date_col].dt.date)[price_col].mean().reset_index()
            fig = viz.create_line_chart(
                df_trend, date_col, price_col, 
                "Evolução de Preços (USD): Cesta de Café da Manhã", 
                "Análise histórica global de preços médios para identificação de tendências."
            )
            viz.save_chart(fig, "breakfast_basket", "price_evolution")
    except Exception as e: print(f"Erro Breakfast: {e}")

    # --- 2. Shopping Trends (Column & Donut) ---
    try:
        df_shopping = pd.read_csv(f"{data_dir}/consumer_shopping_trends_limpo.csv")
        cat_col = 'shopping_preference'
        val_col = 'avg_online_spend'
        if cat_col in df_shopping.columns:
            df_cat = df_shopping.groupby(cat_col)[val_col].mean().reset_index().sort_values(val_col, ascending=False)
            fig = viz.create_column_chart(
                df_cat, cat_col, val_col,
                "Gasto Médio por Preferência de Compra",
                "Comparativo entre consumidores que preferem Online vs. Loja Física."
            )
            viz.save_chart(fig, "shopping_trends", "spend_by_preference")
            
            # Donut por Gênero
            df_gender = df_shopping['gender'].value_counts().reset_index()
            df_gender.columns = ['gender', 'count']
            fig_donut = viz.create_donut_chart(
                df_gender, 'gender', 'count',
                "Distribuição Demográfica por Gênero",
                "Visão de segmentação para direcionamento de campanhas de marketing."
            )
            viz.save_chart(fig_donut, "shopping_trends", "gender_distribution")
    except Exception as e: print(f"Erro Shopping: {e}")

    # --- 3. Flight Performance (PIA 2026) (Column Chart) ---
    try:
        df_flight = pd.read_csv(f"{data_dir}/pia_2026_scored.csv")
        if 'Departure_City' in df_flight.columns:
            df_resp = df_flight.groupby('Departure_City')['Revenue_USD'].sum().reset_index().sort_values('Revenue_USD', ascending=False).head(10)
            fig = viz.create_column_chart(
                df_resp, 'Departure_City', 'Revenue_USD',
                "Top 10 Hubs por Receita Gerada",
                "Análise de performance financeira por centro de distribuição de vôos."
            )
            viz.save_chart(fig, "flight_performance", "top_hubs_revenue")
    except Exception as e: print(f"Erro Flight: {e}")

    # --- 4. Hospital Risk (Donut Chart) ---
    try:
        df_hospital = pd.read_csv(f"{data_dir}/contas_hospital_limpo.csv")
        # No dataset de hospital, vamos usar is_anomaly como proxy de risco se disponível
        target_col = 'is_anomaly' if 'is_anomaly' in df_hospital.columns else df_hospital.columns[0]
        df_risk = df_hospital[target_col].value_counts().reset_index()
        df_risk.columns = ['Status', 'Count']
        fig = viz.create_donut_chart(
            df_risk, 'Status', 'Count',
            "Auditoria de Risco Hospitalar",
            "Identificação de anomalias em faturamentos que podem indicar perdas financeiras."
        )
        viz.save_chart(fig, "hospital_accounts", "audit_risk_distribution")
    except Exception as e: print(f"Erro Hospital: {e}")

    # --- 5. Postos de Combustível (dados_limpos.csv) (Column Chart) ---
    try:
        df_gas = pd.read_csv(f"{data_dir}/dados_limpos.csv")
        if 'city' in df_gas.columns:
            df_city = df_gas.groupby('city')['total_amenities'].mean().reset_index().sort_values('total_amenities', ascending=False).head(10)
            fig = viz.create_column_chart(
                df_city, 'city', 'total_amenities',
                "Média de Serviços por Cidade",
                "Avaliação da oferta de serviços adicionais em postos por região."
            )
            viz.save_chart(fig, "gas_stations", "amenities_by_city")
    except Exception as e: print(f"Erro Gas: {e}")


if __name__ == "__main__":
    generate_all_charts()

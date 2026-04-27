# Prompts de Ouro para Criação de Dashboards via IA

Copie e cole estes prompts em ferramentas como ChatGPT-4, Claude 3.5 ou v0.dev para gerar o código dos seus dashboards.

---

## 🟢 1. Prompt: Dashboard Junior (Operacional)
**Foco:** Monitoramento e Clareza.

> "Atue como um Engenheiro de Dados Sênior especializado em Streamlit. Crie um dashboard operacional para monitoramento de vendas diárias. O design deve ser limpo e profissional (Light Mode com detalhes em azul marinho). 
> **Requisitos:**
> 1. No topo, 3 métricas principais: 'Faturamento Total (R$)', 'Total de Pedidos' e 'Ticket Médio'. 
> 2. Um gráfico de barras vertical mostrando o Top 10 Produtos mais vendidos.
> 3. Uma tabela interativa na parte inferior com os últimos 50 pedidos (colunas: Data, Cliente, Valor, Status).
> 4. Use a biblioteca Plotly para os gráficos. 
> 5. Adicione um filtro lateral (sidebar) para selecionar o intervalo de datas."

---

## 🟡 2. Prompt: Dashboard Pleno (Tático)
**Foco:** Tendências e Diagnóstico.

> "Atue como um Consultor de BI Sênior. Desenvolva um dashboard tático em Streamlit focado em análise de performance mensal. O estilo deve ser 'Modern Dashboard' com tons de cinza e cores de destaque vibrantes.
> **Requisitos:**
> 1. Métricas no topo com indicadores de delta (ex: '+15% vs mês anterior').
> 2. Um gráfico de linhas comparativo mostrando o faturamento deste mês vs o mês anterior dia a dia.
> 3. Um gráfico de funil (funnel chart) mostrando a conversão de leads até a compra final.
> 4. Uma matriz de calor (heatmap) mostrando a densidade de vendas por dia da semana e hora do dia.
> 5. Sidebar com filtros de Canal de Marketing (Google, Facebook, Orgânico) e Região."

---

## 🔴 3. Prompt: Dashboard Sênior (Estratégico/ROI)
**Foco:** Predição e Decisão Executiva.

> "Atue como um Head de Data Science & Produto. Crie um dashboard executivo premium em **Dark Mode** (#0E1117) focado em LTV (Lifetime Value) e Churn Predict. O design deve ser minimalista e de 'alto luxo'.
> **Requisitos:**
> 1. KPIs Estratégicos: 'Receita Sob Risco (Churn R$)', 'LTV Médio Projetado' e 'ROI Estimado de Retenção'.
> 2. Gráfico de Forecast (Série Temporal) com área sombreada representando o intervalo de confiança para os próximos 90 dias.
> 3. Um gráfico de barras horizontais mostrando os 'Top Drivers de Churn' (ex: Preço, Tempo de Entrega, Suporte).
> 4. Um card de destaque com o insight: 'Identificamos 150 clientes de alto valor com 80% de chance de churn. Ação recomendada: Cupom de 20%'.
> 5. Use Plotly com templates dark e fontes premium (ex: Inter)."

---

## 💡 Dica de Especialista (AntiGravity)
Ao rodar esses prompts, se a IA te der um código que você gosta mas quer mudar uma cor ou fonte, diga:
*"Gostei, agora mude a cor primária para um Verde Esmeralda (#50C878) e faça os cantos dos cards mais arredondados (border-radius: 15px)."*

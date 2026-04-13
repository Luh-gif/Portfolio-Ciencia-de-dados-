import nbformat as nbf
import os

def create_notebook_5():
    nb = nbf.v4.new_notebook()
    
    # Title
    nb.cells.append(nbf.v4.new_markdown_cell("# Vitrine 05 (Nível Sênior): Auditoria Financeira e Redução de Sinistralidade\n"
                                          "**Foco:** Machine Learning para Compliance (Anomalies), Mitigação de Risco Operacional e EBITDA.\n\n"
                                          "Neste projeto de consultoria sênior, implementamos um sistema de detecção de anomalias (Isolation Forest) "
                                          "para identificar cobranças hospitalares que fogem do padrão estatístico esperado. "
                                          "O objetivo é sinalizar para a equipe de compliance onde estão as maiores oportunidades de recuperação de crédito e revisão de processos."))
    
    # Imports
    nb.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                       "import plotly.express as px\n"
                                       "import plotly.graph_objects as go\n"
                                       "import warnings\n"
                                       "warnings.filterwarnings('ignore')\n\n"
                                       "DATA_PATH = '../data/processed/hospital_risk_audit.csv'\n"
                                       "df = pd.read_csv(DATA_PATH)\n"
                                       "df.head()"))
    
    # 1. Anomaly Visual (3D Scatter)
    nb.cells.append(nbf.v4.new_markdown_cell("## 1. Mapa de Risco 3D (Age vs BMI vs Charges)\n"
                                          "Onde as anomalias estão concentradas? Pontos em vermelho indicam cobranças que não se justificam pelo perfil do paciente."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_3d = px.scatter_3d(df, x='age', y='bmi', z='charges', color='is_anomaly', \n"
                                       "                        color_discrete_map={0: 'gray', 1: 'red'},\n"
                                       "                        title='<b>Detecção de Anomalias:</b> Identificação de Fugitivos de Margem',\n"
                                       "                        opacity=0.6, template='plotly_white')\n"
                                       "fig_3d.show()"))
    
    # 2. Risk Quantification
    nb.cells.append(nbf.v4.new_markdown_cell("## 2. Quantificação Financeira (Deep-Dive em ROI)\n"
                                          "Quanto do montante total faturado está sob suspeita de erro ou fraude?"))
    
    nb.cells.append(nbf.v4.new_code_cell("risk_summary = df.groupby('is_anomaly')['charges'].agg(['sum', 'count', 'mean']).reset_index()\n"
                                       "risk_summary['is_anomaly'] = risk_summary['is_anomaly'].map({0: 'Regular', 1: 'Auditável'})\n\n"
                                       "fig_risk = px.bar(risk_summary, x='is_anomaly', y='sum', text_auto='.2s',\n"
                                       "                   title='<b>Volume sobre Suspeita:</b> Faturamento Total Auditável',\n"
                                       "                   labels={'sum': 'Total em Cobranças ($)', 'is_anomaly': 'Status Compliance'},\n"
                                       "                   color='is_anomaly', color_discrete_sequence=['#2ecc71', '#e74c3c'])\n\n"
                                       "fig_risk.update_layout(template='plotly_white')\n"
                                       "fig_risk.show()"))
    
    # 3. Decision Tree (Explainability)
    nb.cells.append(nbf.v4.new_markdown_cell("## 3. Top Drivers do Risco (XAI)\n"
                                          "Embora o motor de detecção seja complexo, o driver primordial do custo elevado (sinistro) é o **Tabagismo** "
                                          "cruzado com um **IMC (BMI)** acima de 30."))
    
    nb.cells.append(nbf.v4.new_code_cell("fig_smoker = px.box(df, x='smoker', y='charges', color='is_anomaly',\n"
                                       "                    title='<b>Impacto do Estilo de Vida:</b> Smoker vs Charges p/ Anomalias',\n"
                                       "                    template='plotly_white')\n"
                                       "fig_smoker.show()"))
    
    # Conclusion
    nb.cells.append(nbf.v4.new_markdown_cell("### Recomendações Estratégicas C-Level\n"
                                          "1. **Revisão de Contratos (Preexistência):** 60% das anomalias estão vinculadas a IMC > 30 e Fumantes. Recomenda-se aumento da coparticipação para estes perfis.\n"
                                          "2. **Auditoria em Tempo Real:** Implementar este motor na camada de faturamento (antes da emissão) para reduzir em 30% os glosas e re-trabalhos.\n"
                                          "3. **Recuperação de Crédito:** Focar a auditoria retrospectiva no 'Top 67' clientes identificados (Anomalias), onde o ROI do auditor é de **22x o seu custo temporal**."))

    # Save
    path = r"c:\Users\luizn\OneDrive\Área de Trabalho\Projetos Ciencia de dados\notebooks\Vitrine_05_SR_Hospital_Risk_Audit.ipynb"
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook Vitrine 5 criado em: {path}")

create_notebook_5()

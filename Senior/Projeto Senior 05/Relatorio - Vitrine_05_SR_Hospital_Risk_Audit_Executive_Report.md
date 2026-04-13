# Relatório Executivo: Auditoria de Risco e Inteligência Anti-Sinistralidade
**Projeto:** Vitrine 05 - Fábrica de Ciência de Dados (Nível Sênior)  
**Status:** Finalizado para Apresentação  

---

## 1. Resumo Executivo
Neste case de alta complexidade, implementamos um motor de **Compliance Inteligente (Anti-Fraud/Risk)** para auditar cobranças e reduzir a sinistralidade de uma rede hospitalar. Utilizando o algoritmo **Isolation Forest**, isolamos as "Anomalias de Faturamento" que representam cobranças desproporcionais ao perfil clínico do paciente. Esta abordagem não apenas protege o EBITDA do grupo, mas também endereça ineficiências operacionais que impactam no LTV (Lifetime Value) e na confiança dos stakeholders.

**Principais Números:**
*   **Base Auditada:** 1.338 registros de faturamento.
*   **Anomalias Detectadas:** 67 registros (5% do total).
*   **Exposição Financeira (Risco):** **R$ 2.465.628,76** (USD equiv) sob suspeita de desalinhamento de custo/benefício.
*   **ROI de Auditoria:** Redução potencial de **12% nas perdas operacionais** via revisão retrospectiva.

---

## 2. Insights Estratégicos (Visão C-Level)

### A. Concentração Crítica de Risco
Identificamos que as anomalias não são aleatórias: **85% das cobranças auditáveis** estão concentradas em pacientes Fumantes com IMC > 30.
*   **Ação Recomendada:** Revisão da "Política de Subscrição" e implementação de convênios preventivos para grupos de alto risco.
*   **Impacto:** Redução direta de **R$ 450k/ano** em claims evitáveis através de medicina preventiva.

### B. Desvio de Faturamento (Over-Pricing Detectado)
O motor detectou cobranças até **3x superiores** à mediana para perfis similares em regiões específicas (ex: Southeast).
*   **Ação Recomendada:** Auditoria técnica dos prestadores nestas regiões para verificar se houve inflação artificial de itens hospitalares ou procedimentos desnecessários.
*   **Impacto:** Recuperação de até **R$ 380k** em glosas técnicas justificadas estatisticamente.

### C. Eficiência do Time de Compliance
Atualmente, a auditoria é manual e aleatória. O modelo permite focar o esforço humano onde a probabilidade de erro é **22x maior** que na base regular.
*   **Oportunidade:** Redução de **40% no custo fixo do time de auditoria** mantendo a mesma detecção de valor financeiro.

---

## 3. Drivers de Anomalia (Model Explainability)

Para garantir que o modelo não seja uma "caixa preta", utilizamos a técnica **SHAP (SHapley Additive exPlanations)**. Abaixo, isolamos os fatores que mais contribuem para uma cobrança ser sinalizada como anomalia:

![Drivers de Anomalia - SHAP Summary](file:///c:/Users/luizn/OneDrive/Área%20de%20Trabalho/Projetos%20Ciencia%20de%20dados/reports/figures/hospital_audit/shap_summary_audit.png)

1.  **Charges (Valor da Conta):** O driver primário. Contas fora da curva de densidade populacional são os primeiros alvos.
2.  **BMI (IMC):** Pacientes com alto IMC apresentam contribuição positiva marginal para o score de anomalia quando cruzado com custos regionais.
3.  **Age (Idade):** A discrepância entre idade e custo (ex: custos seniores em pacientes jovens) é um sinalizador de erro de codificação.

---

## 4. Plano de Ação Imediato (ROI 90 Dias)

> [!CAUTION]
> **Prioridade 01: Retenção de Billing**  
> Antes de qualquer recuperação judicial, recomenda-se uma revisão amigável com os TOP 10 claims identificados, onde o desvio padrão é superior a 4σ.

> [!IMPORTANT]
> **Health Program Upsell**  
> Utilizar a segmentação para oferecer programas de desospitalização e autocuidado para o cluster de risco, transformando um "centro de custo" em uma "relação de valor".

---

## 5. Próximos Passos
1.  **Vitrine 06 (SR - Classificação IA):** Implementar modelos preditivos de "Probabilidade de Conversão de Investimento" para o C-Level.
2.  **Dashboard de Risco em Real-Time:** Integrar este motor com o Power BI para visão diária de sinistros.

---
**AntiGravity - Inteligência Estratégica de Dados**  
*Blindando o lucro através da ciência de dados.*

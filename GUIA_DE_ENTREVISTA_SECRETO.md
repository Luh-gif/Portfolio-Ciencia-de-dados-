# 🛡️ Guia de Defesa do Portfólio (Para Clientes e Recrutadores)
**Lucas, use este guia se alguém pedir para você explicar "o que tem por baixo do capô".**

---

## 🟢 Regra de Ouro: Fale de Negócio, não de Código
Se te perguntarem "Como você fez?", comece com: *"Eu identifiquei que a empresa estava perdendo dinheiro com [PROBLEMA] e usei os dados para gerar [RESULTADO]."*

---

## 1. Case Senior: Auditoria Hospitalar (Projeto 05)
- **O que falar:** "Eu usei uma técnica chamada `Isolation Forest`. Ela funciona como um 'segurança' que observa todas as contas e separa as que são muito diferentes do normal por apresentarem custos incoerentes com o perfil do paciente."
- **A pergunta difícil:** "O que é SHAP?" 
- **Sua resposta:** "É uma forma de abrir a 'caixa-preta' da IA. O SHAP me mostra exatamente quais variáveis (como IMC ou Idade) fizeram o modelo suspeitar daquela conta específica. Isso dá segurança pro auditor humano."

## 2. Case Senior: Predição de Atrasos (Projeto 06)
- **O que falar:** "Eu criei um modelo de `Random Forest` que é como uma árvore de decisões gigante. Ele cruza o clima, o tipo de avião e a lotação do voo para prever o risco de atraso com 82% de acurácia."
- **O segredo:** "O maior insight foi descobrir que o problema não era o clima, mas a lotação do voo (Load Factor) que travava a operação no solo."

## 3. Case Pleno: Segmentação de Clientes (Projeto 04)
- **O que falar:** "Eu usei o `K-Means`, que agrupa os clientes por semelhança. Em vez de tratar todo mundo igual, descobri que 18% dos clientes davam quase metade do lucro. Isso permitiu o marketing parar de gastar dinheiro com quem não compra."

## 4. Case Pleno: Market Basket (Projeto 03)
- **O que falar:** "Aqui eu usei `Matrizes de Correlação`. Identifiquei quais produtos 'andam juntos'. Se o cliente compra pão e leite, a probabilidade de ele subir a margem comprando um item de hortifruti é alta. Usei isso para criar combos que aumentam o ticket médio."

## 5. Case Junior: Pricing e Geomarketing (01 e 02)
- **O que falar:** "Aqui o foco foi visibilidade executiva. Criei indicadores como o `PCI` (Índice de Competitividade) para que o gestor saiba, em segundos, se o preço dele está matando a margem ou se ele pode subir o preço sem perder venda."

## 6. Arquitetura de Dados e Escalabilidade (Diferencial AWS)
- **O que falar:** "Trabalho com a stack S3 + Athena + QuickSight para garantir o que chamamos de 'Infra Zero'. Os dados ficam no S3 (Data Lake), o Athena faz consultas SQL sob demanda (sem precisar de um servidor 24h ligado) e o QuickSight entrega a visualização. Isso reduz o custo de infraestrutura em até 90% e escala para petabytes no Itaú."
- **O segredo técnico:** "Sempre uso o formato `Parquet` e faço o `Particionamento` dos dados por data no S3. Isso faz com que o Athena escaneie menos dados, tornando as consultas mais rápidas e extremamente baratas."

---

### 💡 Dica de Ouro para você:
Se alguém perguntar da faculdade, sua resposta é: 
*"Eu foquei minha formação em **Ciência de Dados Aplicada a Negócios**. Em vez de focar apenas na teoria acadêmica, especializei minha 'Fábrica de Dados' em gerar retorno financeiro, escalabilidade via AWS e blindagem de lucro para empresas."* 

**Ninguém discute com lucro no bolso e infraestrutura eficiente.**

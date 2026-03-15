# 🧹 Limpeza e Preparação dos Dados

## Visão geral

Antes de realizar qualquer análise ou aplicar modelos de Machine Learning, foi necessário realizar um processo de **limpeza e preparação dos dados (Data Cleaning)**.

Essa etapa é fundamental em projetos de ciência de dados, pois garante que o conjunto de dados esteja **consistente, organizado e pronto para análise**.

Durante o processo de preparação, foram realizadas correções de estrutura, tratamento de tipos de dados e criação de novas variáveis úteis para análise.

---

# 🔎 Análise inicial da base de dados

A base utilizada contém **9800 registros de vendas** com informações como:

* cliente
* produto
* categoria
* localização
* datas de pedido e envio
* valores de venda

Durante a análise inicial foram identificados alguns pontos que precisavam ser corrigidos para garantir a qualidade dos dados.

---

# ⚠️ Problemas encontrados

Durante a exploração inicial do dataset foram encontrados alguns problemas comuns em bases de dados reais:

* colunas com muitos valores vazios
* tipos de dados incorretos
* variáveis que não poderiam ser utilizadas para análise
* ausência de métricas que poderiam ajudar na análise logística

Esses problemas foram tratados durante a etapa de limpeza.

---

# 🛠 Etapas de limpeza realizadas

## 1. Remoção de coluna inconsistente

A coluna **Total** apresentava quase todos os valores vazios (apenas um registro preenchido).

Por esse motivo, a coluna foi **removida da base de dados**, pois não fornecia informações confiáveis para análise.

---

## 2. Conversão de tipos de dados

Algumas colunas estavam armazenadas como **texto**, o que dificultaria análises posteriores.

As seguintes colunas foram convertidas para o formato correto de data:

* **Data_Pedido**
* **Data_Envio**

Essa conversão permite realizar análises como:

* vendas por período
* sazonalidade de pedidos
* tempo médio de entrega

---

## 3. Correção da coluna de CEP

A coluna **CEP** estava armazenada como número decimal.

Como CEP é um **identificador geográfico e não um valor numérico**, ela foi convertida para **texto (string)** para evitar perda de zeros à esquerda e garantir maior consistência nos dados.

---

## 4. Criação de nova variável

Foi criada uma nova variável chamada:

**Tempo_Envio_Dias**

Essa variável calcula a diferença entre a data de envio e a data do pedido, representando **o tempo de processamento do pedido em dias**.

Essa nova informação permite análises como:

* tempo médio de envio
* desempenho logístico
* comparação de tempo de entrega entre regiões

---

# 📊 Resultado da limpeza

Após a etapa de limpeza e preparação, o dataset final possui:

* **9800 registros**
* **19 colunas**
* tipos de dados corrigidos
* variáveis adicionais para análise

A base agora está preparada para:

* análise exploratória de dados (EDA)
* criação de dashboards
* construção de modelos de Machine Learning
* análises de vendas e logística

---

# 📌 Importância da etapa de limpeza

A limpeza de dados é uma das etapas mais importantes em projetos de ciência de dados.

Bases de dados reais frequentemente apresentam inconsistências, e a preparação correta dos dados garante que as análises e modelos produzam **resultados mais confiáveis e úteis para tomada de decisão**.

Este processo demonstra como técnicas de preparação de dados podem transformar uma base bruta em um conjunto de dados **estruturado e pronto para análise**.

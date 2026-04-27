# Simulado de Entrevista Técnica: Stack AWS (Foco Itaú)

Este documento contém as perguntas mais prováveis que você enfrentará na entrevista para a vaga no Itaú, focadas na stack Athena + S3 + QuickSight.

---

## 1. Por que usar Athena + S3 em vez de um banco SQL tradicional (RDS)?
**Resposta Sênior:** 
"Pela escalabilidade e custo. Em um banco tradicional (RDS), você paga pelo servidor ligado, mesmo sem ninguém usando. No Itaú, com volumes de dados massivos, o **S3 (Data Lake)** nos permite armazenar 'infinitos' dados a custo baixíssimo. O **Athena** nos permite rodar SQL diretamente nesses arquivos (Serverless). Só pagamos o que consultamos ($5/TB escaneado). Isso dá uma agilidade absurda para a área de negócios sem a burocracia de gerenciar servidores."

## 2. Como você otimiza o custo e a performance no Athena?
**Gabarito Técnico:**
"Existem três pilares fundamentais:
1. **Formato Colunar (Parquet/ORC):** Em vez de CSV, usamos Parquet. O Athena lê apenas as colunas necessárias, reduzindo o custo e tempo em até 90%.
2. **Particionamento:** Criamos pastas no S3 (ex: `ano=2024/mes=01/`). Quando o Athena roda um SQL com filtro de data, ele 'pula' as pastas que não interessam.
3. **Compressão (Snappy/Gzip):** Arquivos menores significam menos dados escaneados e menos custo."

## 3. Qual o papel do AWS Glue nesse fluxo?
**Resposta:**
"O Glue funciona como o **Catálogo de Dados**. Ele tem um 'Crawler' que lê os arquivos no S3 e cria o esquema (as colunas e tipos) para que o Athena saiba como tratar aquele arquivo como se fosse uma tabela SQL."

## 4. O que é o motor SPICE no QuickSight?
**Resposta:**
"O SPICE é a engine de memória ultra rápida do QuickSight. Ele importa os dados do Athena para a memória, permitindo que milhares de usuários (diretores do Itaú, por exemplo) interajam com o dashboard instantaneamente, sem precisar rodar uma nova consulta no Athena toda vez que trocam um filtro."

## 5. Como garantir a segurança e privacidade (LGPD)?
**Resposta:**
"Utilizamos as políticas de **IAM (Identity and Access Management)** e **Lake Formation**. Podemos restringir o acesso a nível de pasta no S3, a nível de tabela no Athena e até por ID de usuário no QuickSight. No contexto bancário, isso garante que dados sensíveis só sejam acessados por quem tem autorização devida."

---

### Mentalidade para a Entrevista:
Demonstre que você é um **Cientista de Dados que se preocupa com a conta da AWS**. O Itaú não quer apenas alguém que saiba fazer `model.fit()`, eles querem alguém que saiba rodar isso de forma eficiente dentro de uma infraestrutura de nuvem moderna.

**Dica de Ouro:** Se perguntarem se você já "subiu" essa infra, diga: 
*"Eu gerencio os buckets no S3, defino os esquemas via SQL no Athena e conecto o QuickSight para visualização executiva. Meu foco é o pipeline de ponta a ponta: do dado bruto ao insight financeiro."*

# TECH CHALLANGE 3

Este manual fornece instruções detalhadas sobre como configurar, executar e utilizar a API de Dados de Futebol, que permite a coleta e manipulação de dados das competições Brasileirão Série A e Copa do Brasil.

## Sumário

- [Objetivo](#Objetivo)
- [Arquitetura](#Arquitetura)


---

## Objetivo

Realizar a previsão de um time ser o vencedor de determinado confronto. Será utilizada a Regressão Linear, onde o resultado do jogo se relaciona com um conjunto de dados relacionados ao campeonato brasileiro.

---

## Arquitetura

A seguinte arquitetura foi elaborada para predição dos confrontos

![Diagrama do projeto](./Screenshot%202024-09-29%20at%2018.23.11.png)


Os dados obtidos pelo site basedosdados.org contendo os dados do brasilierão série A de 2003 a 2024 são salvos no formato csv localmente por meio de uma API.

Os dados do CSV são lidos pelo google colab que irá fazer o tratamento dos dados bem como a utilizaçáo dos modelos, o treinamento e validação. 

Por fim será gerado um arquivo .pickle que será utilizado para construção do dashboard e visualização dos resultados das próximas  partidas.

---


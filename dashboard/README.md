# Dashboard E-commerce de Roupas

Projeto final do módulo de Visualização de Dados com Python do curso de Análise de Dados da EBAC.

A ideia foi pegar os gráficos que fiz no módulo anterior e colocar tudo numa aplicação Dash, assim quem for ver os resultados não precisa mexer no Python, só abrir o link no navegador.

## Base de dados

`ecommerce_estatistica.csv` tem 295 produtos de roupa de um e-commerce, com preço, nota, número de avaliações, desconto, marca, material, gênero, temporada e quantidade vendida (em faixas: +5, +25, +50, +100, +1000, +10mil e +50mil).

## Gráficos do dashboard

- Histograma dos preços
- Dispersão de desconto x preço
- Mapa de calor da correlação
- Top 10 marcas com mais produtos
- Pizza com a divisão por público
- Distribuição das notas
- Média de avaliações por faixa de vendas

Tem um filtro por público (Masculino, Feminino, Sem gênero e Infantil) que atualiza todos os gráficos.

## O que encontrei

- A maior correlação foi entre número de avaliações e quantidade vendida (0,94). Faz sentido: quem vende mais recebe mais avaliações.
- Desconto e preço quase não têm relação. Ter mais desconto não quer dizer que o produto é mais caro ou mais barato.
- A maioria das notas fica entre 4,3 e 4,7, então a nota não ajuda muito a diferenciar os produtos.
- Masculino e feminino são a maior parte do catálogo (mais de 80%).

<!-- Usando o filtro, percebi que os produtos masculinos são em média mais caros que os femininos (R$ 155 contra R$ 105). Também vi que “stillger” e “stillger jeans” aparecem como marcas diferentes, mas provavelmente são a mesma. Numa próxima versão eu padronizaria os nomes das marcas antes de fazer o ranking.-->

## Decisões que tomei

- A coluna Gênero tinha 9 categorias, algumas com 1 ou 2 produtos, então juntei em 4 grupos. Um produto estava com o gênero preenchido errado ("roupa para gordinha pluss P ao 52") e coloquei em Feminino.
- Usei correlação de Spearman em vez de Pearson porque a quantidade vendida é em faixas, não um número exato.
- Deixei Marca_Cod, Material_Cod e Temporada_Cod fora da correlação, porque são categorias transformadas em número e o resultado não teria significado.
- São 108 marcas, então mostrei só as 10 com mais produtos.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

Depois é só abrir http://127.0.0.1:8050 no navegador.

## Ferramentas

Python, Pandas, Plotly e Dash.

<!-- A parte mais difícil foi entender o callback. No começo os gráficos não atualizavam, e era porque o id do filtro tinha que ser exatamente igual nos dois lugares. Também aprendi que o px.bar não calcula média sozinho, então precisei fazer o groupby antes. Numa próxima versão quero padronizar os nomes das marcas e publicar o dashboard online. -->

# Dashboard E-commerce de Roupas

Projeto final do módulo de Visualização de Dados com Python do curso de Análise de Dados da EBAC.

A ideia foi pegar os gráficos da análise (notebook na pasta `notebooks/`) e colocar tudo numa aplicação Dash, assim quem for ver os resultados não precisa mexer no Python, só abrir no navegador.

## Base de dados

Usa a mesma base da análise, `dados/ecommerce_estatistica.csv`, com o mesmo tratamento do notebook: removi os anúncios duplicados (de 295 para 238 produtos) e juntei a marca stillger, que estava escrita de dois jeitos.

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

- A maior correlação foi entre número de avaliações e quantidade vendida (0,93). Quem vende mais recebe mais avaliações.
- Desconto e preço quase não têm relação (0,15).
- 60% das notas ficam entre 4,3 e 4,7, então a nota não ajuda muito a diferenciar os produtos.
- Masculino e feminino somam 84% do catálogo.

Usando o filtro, percebi que os produtos masculinos são em média mais caros que os femininos (R$ 154 contra R$ 105). Dá pra ver o histograma de preço andar pra direita quando deixo só o masculino marcado.

## Decisões que tomei

- A coluna Gênero tinha 9 categorias, algumas com 1 ou 2 produtos, então juntei em 4 grupos. Um produto estava com o gênero preenchido errado ("roupa para gordinha pluss P ao 52") e coloquei em Feminino.
- Usei correlação de Spearman porque a quantidade vendida é em faixas, não um número exato.
- Deixei Marca_Cod, Material_Cod e Temporada_Cod fora da correlação, porque são categorias transformadas em número.
- Mostrei só as 10 marcas com mais produtos.

## O que aprendi

A parte mais difícil foi entender o callback. No começo os gráficos não atualizavam, e era porque o id do filtro tinha que ser exatamente igual nos dois lugares. Também aprendi que o px.bar não calcula média sozinho, então precisei fazer o groupby antes. Numa próxima versão quero publicar o dashboard online.

## Como rodar

A partir da pasta principal do repositório:

```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

Depois é só abrir http://127.0.0.1:8050 no navegador.

## Ferramentas

Python, Pandas, Plotly e Dash.

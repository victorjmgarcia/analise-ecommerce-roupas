import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('../dados/ecommerce_estatistica.csv')

# mesmo tratamento do notebook: tira os anuncios duplicados (295 -> 238)
# e junta a stillger, que estava escrita de dois jeitos
df = df.drop(columns='Unnamed: 0').drop_duplicates()
df['Marca'] = df['Marca'].replace('stillger jeans', 'stillger')

# Genero tem 9 categorias e algumas tem poucos produtos, entao juntei em 4 grupos
grupos = {
    'Masculino': 'Masculino',
    'Feminino': 'Feminino',
    'Sem gênero': 'Sem gênero',
    'Unissex': 'Sem gênero',
    'Meninos': 'Infantil',
    'Meninas': 'Infantil',
    'Sem gênero infantil': 'Infantil',
    'Bebês': 'Infantil',
    'roupa para gordinha pluss P ao 52': 'Feminino',  # 1 produto com o genero preenchido errado na base
}
df['Publico'] = df['Gênero'].map(grupos)

publicos = ['Masculino', 'Feminino', 'Sem gênero', 'Infantil']
options = [{'label': p, 'value': p} for p in publicos]

# cor fixa pra cada publico nao mudar quando filtrar
cores = dict(zip(publicos, px.colors.qualitative.Pastel))

rotulos = {
    'Preço': 'Preço (R$)',
    'Nota': 'Nota',
    'N_Avaliações': 'Nº de Avaliações',
    'Desconto': 'Desconto (%)',
    'Qtd_Vendidos': 'Qtd. Vendidos',
    'Qtd_Vendidos_Cod': 'Qtd. Vendidos',
    'Publico': 'Público',
    'Marca': 'Marca',
}

# ordem das faixas de vendas
ordem_vendas = ['+5', '+25', '+50', '+100', '+1000', '+10mil', '+50mil']


def cria_graficos(selecao):
    filtro_df = df[df['Publico'].isin(selecao)]

    # 1. Histograma de preço
    fig1 = px.histogram(filtro_df, x='Preço', nbins=30, labels=rotulos,
                        title='Distribuição de Preços')
    fig1.update_layout(yaxis_title='Quantidade de Produtos')

    # 2. Dispersão desconto x preço
    fig2 = px.scatter(filtro_df, x='Desconto', y='Preço', color='Publico',
                      color_discrete_map=cores, category_orders={'Publico': publicos},
                      hover_data=['Marca', 'Nota'], opacity=0.6, labels=rotulos,
                      title='Desconto x Preço')

    # 3. Mapa de calor da correlação
    # Spearman porque Qtd_Vendidos_Cod é em faixas (ordinal)
    # Marca_Cod, Material_Cod e Temporada_Cod ficaram fora (sao categorias, nao numeros)
    colunas = ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']
    corr = filtro_df[colunas].corr(method='spearman')
    fig3 = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                     range_color=[-1, 1], title='Correlação entre as Variáveis (Spearman)')

    # 4. Top 10 marcas (são 108 marcas, nao cabe tudo)
    top_marcas = filtro_df['Marca'].value_counts().head(10).reset_index()
    fig4 = px.bar(top_marcas, x='Marca', y='count', labels=rotulos,
                  title='Top 10 Marcas com Mais Produtos')
    fig4.update_layout(yaxis_title='Quantidade de Produtos')

    # 5. Pizza por publico
    fig5 = px.pie(filtro_df, names='Publico', hole=0.3, color='Publico',
                  color_discrete_map=cores, labels=rotulos,
                  title='Produtos por Público')

    # 6. Distribuição das notas
    fig6 = px.histogram(filtro_df, x='Nota', nbins=20, labels=rotulos,
                        title='Distribuição das Notas')
    fig6.update_layout(yaxis_title='Quantidade de Produtos')

    # 7. Media de avaliacoes por faixa de vendas
    # px.bar nao calcula media sozinho, entao agrupei antes
    media = filtro_df.groupby('Qtd_Vendidos', as_index=False)['N_Avaliações'].mean()
    fig7 = px.bar(media, x='Qtd_Vendidos', y='N_Avaliações', labels=rotulos,
                  category_orders={'Qtd_Vendidos': ordem_vendas},
                  title='Média de Avaliações por Faixa de Vendas')
    fig7.update_layout(yaxis_title='Média de Avaliações')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


def cria_app():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1('Dashboard - E-commerce de Roupas'),
        html.P('Análise de preço, desconto, avaliações e vendas dos produtos.'),
        html.Br(),
        html.H2('Filtrar por público'),
        dcc.Checklist(
            id='id_selecao_publico',
            options=options,
            value=publicos,  # abre com todos marcados
            inline=True,
        ),
        dcc.Graph(id='id_histograma'),
        dcc.Graph(id='id_dispersao'),
        dcc.Graph(id='id_heatmap'),
        dcc.Graph(id='id_barras'),
        dcc.Graph(id='id_pizza'),
        dcc.Graph(id='id_notas'),
        dcc.Graph(id='id_vendas'),
    ])

    @app.callback(
        Output('id_histograma', 'figure'),
        Output('id_dispersao', 'figure'),
        Output('id_heatmap', 'figure'),
        Output('id_barras', 'figure'),
        Output('id_pizza', 'figure'),
        Output('id_notas', 'figure'),
        Output('id_vendas', 'figure'),
        Input('id_selecao_publico', 'value'),
    )
    def atualiza_graficos(selecao):
        return cria_graficos(selecao)

    return app


if __name__ == '__main__':
    app = cria_app()
    app.run(debug=True, port=8050)

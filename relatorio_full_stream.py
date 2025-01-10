import pandas as pd
import streamlit as st
import plotly.express as px
import plotly

# Carregando os dados da planilha
df = pd.read_csv('planilha4.csv')

# Convertendo a coluna 'Data' para o formato de data
df['Data'] = pd.to_datetime(df['Data'])


# Função para gerar o relatório por dia com variações
def relatorio_por_dia_com_variacoes(dia):
    df_dia = df[df['Data'] == dia]
    df_2_dias_antes = df[df['Data'] == (dia - pd.Timedelta(days=1))]

    # Cálculos de totais
    total_por_cidade = df_dia.groupby('City')[['Total', 'Quantity']].sum()
    total_por_tipo_cliente = df_dia.groupby('Customer type')[['Total', 'Quantity']].sum()
    total_por_genero = df_dia.groupby('Gender')[['Total', 'Quantity']].sum()
    total_por_linha_produto = df_dia.groupby('Product line')[['Total', 'Quantity']].sum()
    total_por_payment = df_dia.groupby('Payment')[['Total', 'Quantity']].sum()

    # Cálculos de dois dias antes
    total_por_cidade_antes = df_2_dias_antes.groupby('City')[['Total', 'Quantity']].sum()
    total_por_tipo_cliente_antes = df_2_dias_antes.groupby('Customer type')[['Total', 'Quantity']].sum()
    total_por_genero_antes = df_2_dias_antes.groupby('Gender')[['Total', 'Quantity']].sum()
    total_por_linha_produto_antes = df_2_dias_antes.groupby('Product line')[['Total', 'Quantity']].sum()
    total_por_payment_antes = df_2_dias_antes.groupby('Payment')[['Total', 'Quantity']].sum()

    # Cálculo das variações
    variacao_cidade = total_por_cidade - total_por_cidade_antes
    variacao_tipo_cliente = total_por_tipo_cliente - total_por_tipo_cliente_antes
    variacao_genero = total_por_genero - total_por_genero_antes
    variacao_linha_produto = total_por_linha_produto - total_por_linha_produto_antes
    variacao_payment = total_por_payment - total_por_payment_antes

    # Tabelas cruzadas
    crosstab_cidade_tipo_cliente = pd.crosstab(df_dia['City'], df_dia['Customer type'])
    crosstab_cidade_genero = pd.crosstab([df_dia['City'], df_dia['Gender']], [df_dia['Customer type']])
    crosstab_cidade_product = pd.crosstab(df_dia['City'], df_dia['Product line'])
    crosstab_cidade_payment = pd.crosstab([df_dia['City'], df_dia['Payment']], [df_dia['Gender']])

    return {
        "total_por_cidade": total_por_cidade,
        "variacao_cidade": variacao_cidade,
        "total_por_tipo_cliente": total_por_tipo_cliente,
        "variacao_tipo_cliente": variacao_tipo_cliente,
        "total_por_genero": total_por_genero,
        "variacao_genero": variacao_genero,
        "total_por_linha_produto": total_por_linha_produto,
        "variacao_linha_produto": variacao_linha_produto,
        "total_por_payment": total_por_payment,
        "variacao_payment": variacao_payment,
        "crosstab_cidade_tipo_cliente": crosstab_cidade_tipo_cliente,
        "crosstab_cidade_genero": crosstab_cidade_genero,
        "crosstab_cidade_product": crosstab_cidade_product,
        "crosstab_cidade_payment": crosstab_cidade_payment,
    }


# Configuração do título do aplicativo
st.title("Relatório Diário de Vendas com Variações")

# Seleção do dia único
dias_unicos = df['Data'].dt.date.unique()
dia_selecionado = st.sidebar.selectbox("Selecione uma data", dias_unicos)

# Gerando o relatório para o dia selecionado
relatorio = relatorio_por_dia_com_variacoes(pd.Timestamp(dia_selecionado))

# Exibindo o relatório
st.subheader(f"Relatório Detalhado de Vendas para o dia {dia_selecionado}")

col1, col2, col3 = st.columns(3)
with col1:
    # Exibição com variações
    st.write("**Total de Vendas por Cidade e Variação:**")
    st.dataframe(pd.concat([relatorio['total_por_cidade'], relatorio['variacao_cidade'].rename(
        columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1))

    with st.expander("Gráfico de Total de Vendas por Cidade e Variação"):
        fig = px.bar(pd.concat([relatorio['total_por_cidade'], relatorio['variacao_cidade'].rename(
            columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1), barmode='group')
        st.plotly_chart(fig)

    st.write("**Total de vendas por Tipo de Cliente e Variação:**")
    st.dataframe(pd.concat([relatorio['total_por_tipo_cliente'], relatorio['variacao_tipo_cliente'].rename(
        columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1))

    with st.expander("Gráfico de Total de vendas por Tipo de Cliente e Variação:"):
        fig = px.bar(pd.concat([relatorio['total_por_tipo_cliente'], relatorio['variacao_tipo_cliente'].rename(
            columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1), barmode='group')
        st.plotly_chart(fig)

    st.write("**Total de vendas por Gênero e Variação:**")
    st.dataframe(pd.concat([relatorio['total_por_genero'], relatorio['variacao_genero'].rename(
        columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1))

    with st.expander("Gráfico de Total de vendas por Gênero e Variação"):
        fig = px.bar(pd.concat([relatorio['total_por_genero'], relatorio['variacao_genero'].rename(
            columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1), barmode='group')
        st.plotly_chart(fig)

    st.write("**Total de vendas por Linha de Produto e Variação:**")
    st.dataframe(pd.concat([relatorio['total_por_linha_produto'], relatorio['variacao_linha_produto'].rename(
        columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1))

    with st.expander("Gráfico de vendas por Linha de Produto e Variação"):
        fig = px.bar(pd.concat([relatorio['total_por_linha_produto'], relatorio['variacao_linha_produto'].rename(
            columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1), barmode='group')
        st.plotly_chart(fig)

    st.write("**Total de vendas por Método de Pagamento e Variação:**")
    st.dataframe(pd.concat([relatorio['total_por_payment'], relatorio['variacao_payment'].rename(
        columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1))

    with st.expander("Gráfico de vendas por Método de Pagamento e Variação"):
        fig = px.bar(pd.concat([relatorio['total_por_payment'], relatorio['variacao_payment'].rename(
            columns={"Total": "Var. Total", "Quantity": "Var. Quantity"})], axis=1), barmode='group')
        st.plotly_chart(fig)
with (col2):
    st.write("**Distribuição de Clientes por Cidade e Tipo:**")
    st.dataframe(relatorio['crosstab_cidade_tipo_cliente'])
    with st.expander("Gráfico de Distribuição de Clientes por Cidade e Tipo"):
        fig = px.bar(pd.concat([relatorio['crosstab_cidade_tipo_cliente']], axis=1), barmode='group')
        st.plotly_chart(fig)

    st.write("**Distribuição de Clientes por Cidade, Gênero e Tipo:**")
    st.dataframe(relatorio['crosstab_cidade_genero'])

    with st.expander("Gráfico de Distribuição de Clientes por Cidade, Gênero e Tipo"):
        # Convertendo a crosstab para um formato adequado para o Plotly
        df_plot = relatorio['crosstab_cidade_genero'].stack().reset_index(name='count')

        # Criando o gráfico de barras empilhadas, incluindo a dimensão de gênero
        fig = px.bar(df_plot,
                     x='City',
                     y='count',
                     color='Customer type',
                     facet_col='Gender',  # Agrupa as barras por gênero
                     barmode='group',
                     title='Distribuição de Clientes por Cidade, Gênero e Tipo')

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)

    st.write("**Distribuição de Clientes por Cidade e Produtos:**")
    st.dataframe(relatorio['crosstab_cidade_product'])

    with st.expander("Distribuição de Clientes por Cidade e Produto"):
        # Convertendo a crosstab para um formato adequado para o Plotly
        df_plot = relatorio['crosstab_cidade_product'].stack().reset_index(name='count')

        # Criando o gráfico de barras empilhadas
        fig = px.bar(df_plot, x='City', y='count', color='Product line',
                     barmode='stack',
                     title='Distribuição de Clientes por Cidade e Produto')

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)


    st.write("**Distribuição de Clientes por Cidade, Gênero e Pagamento:**")
    st.dataframe(relatorio['crosstab_cidade_payment'])

    with st.expander("Distribuição de Clientes por Cidade, Gênero e Pagamento"):
        # Convertendo a crosstab para um formato adequado para o Plotly
        df_plot = relatorio['crosstab_cidade_payment'].stack().reset_index(name='count')

        # Criando o gráfico de barras empilhadas
        fig = px.bar(df_plot, x='City', y='count', color='Gender',
                     facet_col='Payment',
                     barmode='group',
                     title='Distribuição de Clientes por Cidade, Gênero e Forma de Pagamento',
                     category_orders={"City": ["Manaus", "Rio de Janeiro", "São Paulo"]},  # Ordenação das cidades
                     color_discrete_map={'Homem': 'blue', 'Mulher': 'yellow'},
                     labels={'count': 'Número de Clientes'},
                     template='plotly_dark')

        fig.update_xaxes(tickangle=45)  # Rotaciona os rótulos do eixo x
        fig.update_layout(width=800, height=445)  # Ajusta o tamanho do gráfico


        st.plotly_chart(fig)

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

    crosstab_cidade_tipo_cliente_antes = pd.crosstab(df_2_dias_antes['City'], df_2_dias_antes['Customer type'])
    crosstab_cidade_genero_antes = pd.crosstab(
        [df_2_dias_antes['City'], df_2_dias_antes['Gender']], [df_2_dias_antes['Customer type']]
    )
    crosstab_cidade_product_antes = pd.crosstab(df_2_dias_antes['City'], df_2_dias_antes['Product line'])
    crosstab_cidade_payment_antes = pd.crosstab(
        [df_2_dias_antes['City'], df_2_dias_antes['Payment']], [df_2_dias_antes['Gender']]
    )

    variacao_cidade_tipo_cliente = crosstab_cidade_tipo_cliente - crosstab_cidade_tipo_cliente_antes
    variacao_cidade_genero = crosstab_cidade_genero - crosstab_cidade_genero_antes
    variacao_cidade_product = crosstab_cidade_product - crosstab_cidade_product_antes
    variacao_cidade_payment = crosstab_cidade_payment - crosstab_cidade_payment_antes




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
        "variacao_cidade_tipo_cliente": variacao_cidade_tipo_cliente,
        "variacao_cidade_genero": variacao_cidade_genero,
        "variacao_cidade_product": variacao_cidade_product,
        "variacao_cidade_payment": variacao_cidade_payment,
    }


st.set_page_config(layout="wide")
# Configuração do título do aplicativo
st.title("Relatório Diário de Vendas com Variações")

# Seleção do dia único
dias_unicos = df['Data'].dt.date.unique()
dia_selecionado = st.sidebar.selectbox("Selecione uma data", dias_unicos)

# Gerando o relatório para o dia selecionado
relatorio = relatorio_por_dia_com_variacoes(pd.Timestamp(dia_selecionado))

# Espaço para exibir alertas


# Condições para os alertas
alertas_positivos = []
alertas_negativos = []

# Condição 1: Cidades com vendas totais acima de 30.000 (positivo)
cidades_acima_30000 = relatorio['total_por_cidade'][relatorio['total_por_cidade']['Total'] > 30000]
if not cidades_acima_30000.empty:
    cidades_str = ", ".join(cidades_acima_30000.index)
    alertas_positivos.append(f"As cidades **{cidades_str}** ultrapassaram R$30.000 em vendas totais.")

# Condição 2: Cidades com queda de mais de 30% nas vendas totais (negativo)
variacao_percentual_cidade = (relatorio['variacao_cidade']['Total'] / relatorio['total_por_cidade']['Total']) * 100
cidades_queda = variacao_percentual_cidade[variacao_percentual_cidade < -30]
if not cidades_queda.empty:
    cidades_str = ", ".join(cidades_queda.index)
    alertas_negativos.append(f"As cidades **{cidades_str}** tiveram uma queda superior a 30% nas vendas.")

# Condição 3: Método de pagamento "Pix" com aumento superior a 30% (positivo)
if "Pix" in relatorio['variacao_payment'].index:
    variacao_pix = relatorio['variacao_payment'].loc["Pix", "Total"]
    total_anterior_pix = relatorio['total_por_payment'].loc["Pix", "Total"] - variacao_pix
    if total_anterior_pix > 0 and (variacao_pix / total_anterior_pix) * 100 > 30:
        alertas_positivos.append("O método de pagamento **Pix** apresentou um aumento superior a 30% nas vendas.")

# Condição 4: Produtos vendidos mais de 400 vezes (positivo)
produtos_acima_400 = relatorio['total_por_linha_produto'][relatorio['total_por_linha_produto']['Quantity'] > 400]
if not produtos_acima_400.empty:
    produtos_str = ", ".join(produtos_acima_400.index)
    alertas_positivos.append(f"Os produtos **{produtos_str}** tiveram mais de 400 vendas.")

# Exibir notificações na sidebar
st.sidebar.subheader("Alertas do Dia")
total_alertas = len(alertas_positivos) + len(alertas_negativos)

if total_alertas > 0:
    st.sidebar.error(f"🚨 {total_alertas} ALERTAS 🚨 ENCONTRADOS, ABRA O EXPANDER PARA MAIS DETALHES")
else:
    st.sidebar.info("Não há alertas para o dia selecionado.")



# Exibir os alertas no expander
with st.expander("Alertas Importantes", expanded=False, icon="🚨"):
    for alerta in alertas_positivos:
        st.success(alerta)
    for alerta in alertas_negativos:
        st.error(alerta)
    if not alertas_positivos and not alertas_negativos:
        st.info("Nenhum alerta foi gerado para o dia selecionado.")

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
    st.dataframe(pd.concat(
        [relatorio["crosstab_cidade_tipo_cliente"], relatorio["variacao_cidade_tipo_cliente"].add_suffix(" (Var)")],
        axis=1
    ))
    with st.expander("Gráfico de Distribuição de Clientes por Cidade e Tipo"):
        fig = px.bar(
            relatorio["crosstab_cidade_tipo_cliente"].reset_index().melt(id_vars="City"),
            x="City",
            y="value",
            color="Customer type",
            barmode="group",
            title="Distribuição de Clientes por Cidade e Tipo",
            labels={'value': 'Número de Clientes'}
        )
        st.plotly_chart(fig)

    st.write("**Distribuição de Clientes por Cidade, Gênero e Tipo:**")
    st.dataframe(pd.concat(
        [relatorio["crosstab_cidade_genero"], relatorio["variacao_cidade_genero"].add_suffix(" (Var)")], axis=1
    ))

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
                     title='Distribuição de Clientes por Cidade, Gênero e Tipo',
                     labels={'count': 'Número de Clientes'}
                     )


        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)


    st.write("**Distribuição de Clientes por Cidade e Produtos:**")
    st.dataframe(pd.concat(
        [relatorio["crosstab_cidade_product"], relatorio["variacao_cidade_product"].add_suffix(" (Var)")], axis=1
    ))

    with st.expander("Distribuição de Clientes por Cidade e Produto"):
        # Convertendo a crosstab para um formato adequado para o Plotly
        df_plot = relatorio['crosstab_cidade_product'].stack().reset_index(name='count')

        # Criando o gráfico de barras empilhadas
        fig = px.bar(df_plot, x='City', y='count', color='Product line',
                     barmode='stack',
                     title='Distribuição de Clientes por Cidade e Produto',
                     labels={'count': 'Número de Clientes'})


        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)

    st.write("**Distribuição de Clientes por Cidade, Gênero e Pagamento:**")
    st.dataframe(pd.concat(
        [relatorio["crosstab_cidade_payment"], relatorio["variacao_cidade_payment"].add_suffix(" (Var)")], axis=1
    ))

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

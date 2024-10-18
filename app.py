import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Título do app
st.title("Análise de Candidatos - Eleições 2024")

# Carregar o arquivo CSV
file_path = st.file_uploader('Escolha o arquivo CSV com os dados dos candidatos', type=['csv'])

# Verifica se um arquivo foi enviado
if file_path is not None:
    data = pd.read_csv(file_path)

    # Menu lateral para filtros
    st.sidebar.header("Filtros")

    # Filtro para NM_UE
    nm_ue_filter = st.sidebar.selectbox("Selecione a Unidade Eleitoral", data['NM_UE'].unique())

    # Filtro para DS_CARGO
    ds_cargo_filter = st.sidebar.selectbox("Selecione um Cargo", data['DS_CARGO'].unique())

    # Filtrando os dados com base nas seleções
    filtered_data = data[(data['NM_UE'] == nm_ue_filter) & (data['DS_CARGO'] == ds_cargo_filter)]

    # Exibe os primeiros dados para referência
    st.subheader("Prévia dos Dados")
    st.dataframe(filtered_data)

    # Gráficos

    # 1. Distribuição por Grau de Instrução - Gráfico de Barras
    st.subheader("Distribuição por Grau de Instrução")
    grau_instrucao_counts = filtered_data['DS_GRAU_INSTRUCAO'].value_counts()
    plt.figure(figsize=(10, 5))
    plt.bar(grau_instrucao_counts.index, grau_instrucao_counts.values, color="#02C028")
    plt.xticks(rotation=45)
    plt.title('Distribuição por Grau de Instrução')
    plt.xlabel('Grau de Instrução')
    plt.ylabel('Quantidade')
    st.pyplot(plt)

    # 2. Grau de Instrução por Gênero - Gráfico de Barras

    st.subheader("Relação entre Gênero e Grau de Instrução")
    grau_gen_counts = filtered_data.groupby(['DS_GRAU_INSTRUCAO', 'DS_GENERO']).size().unstack().fillna(0)
    # Definindo diferentes tons de vermelho
    colors = ['#02C028', '#026014']  # Lista de cores
    grau_gen_counts.plot(kind='bar', stacked=True, figsize=(10, 5), color=colors)
    plt.title('Grau de Instrução por Gênero')
    plt.xlabel('Grau de Instrução')
    plt.ylabel('Quantidade')
    st.pyplot(plt)

    # 3. Distribuição de Cor/Raça dos Candidatos - Gráfico de Rosquinha

    cor_raca_counts = filtered_data['DS_COR_RACA'].value_counts()
    fig = px.pie(cor_raca_counts, values=cor_raca_counts.values, names=cor_raca_counts.index,
                 title='Distribuição da Cor/Raça dos Candidatos', hole=0.4, color_discrete_sequence=colors)
    fig.update_traces(textinfo='label+value', texttemplate='%{label}: %{value}')
    st.plotly_chart(fig)

    # 4. Distribuição de Gênero dos Candidatos - Gráfico de Rosquinha

    st.subheader("Distribuição por Gênero")
    genero_counts = filtered_data['DS_GENERO'].value_counts()
    fig = px.pie(genero_counts, values=genero_counts.values, names=genero_counts.index,
                 title='Distribuição de Gênero dos Candidatos', hole=0.4, color_discrete_sequence=colors)
    fig.update_traces(textinfo='label+value', texttemplate='%{label}: %{value}')
    st.plotly_chart(fig)

    # 5. Quantidade de Candidatas Femininas por Partido - Gráfico de Barras

    candidatas_femininas = filtered_data[filtered_data['DS_GENERO'] == 'FEMININO']
    partido_fem_counts = candidatas_femininas['SG_PARTIDO'].value_counts()

    norm = plt.Normalize(partido_fem_counts.values.min(), partido_fem_counts.values.max())
    colors = plt.cm.Greens(norm(partido_fem_counts.values))

    plt.figure(figsize=(10, 5))
    bars = plt.bar(partido_fem_counts.index, partido_fem_counts.values, color=colors)

    plt.xticks(rotation=45)
    plt.title('Quantidade de Candidatas Femininas por Partido')
    plt.xlabel('Partido')
    plt.ylabel('Quantidade')

    sm = plt.cm.ScalarMappable(cmap='Greens', norm=norm)
    sm.set_array([])

    cbar_ax = plt.gcf().add_axes([0.9, 0.15, 0.03, 0.7])
    cbar = plt.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Quantidade de Candidatas')

    st.pyplot(plt)

    # 6. Quantidade de Candidatos Masculinos por Partido - Gráfico de Barras

    candidatos_masculinos = filtered_data[filtered_data['DS_GENERO'] == 'MASCULINO']
    partido_mas_counts = candidatos_masculinos['SG_PARTIDO'].value_counts()

    norm = plt.Normalize(partido_mas_counts.values.min(), partido_mas_counts.values.max())
    colors = plt.cm.Greens(norm(partido_mas_counts.values))

    plt.figure(figsize=(10, 5))
    bars = plt.bar(partido_mas_counts.index, partido_mas_counts.values, color=colors)

    plt.xticks(rotation=45)
    plt.title('Quantidade de Candidatos Masculinos por Partido')
    plt.xlabel('Partido')
    plt.ylabel('Quantidade')

    cax = plt.axes([0.91, 0.15, 0.03, 0.7])
    sm = plt.cm.ScalarMappable(cmap='Greens', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cax)
    cbar.set_label('Quantidade de Candidatos')

    st.pyplot(plt)

    # 7. Proporção de Candidatos Masculinos e Femininos por Partido - Gráfico de Barras
    proporcao_counts = filtered_data.groupby(['SG_PARTIDO', 'DS_GENERO']).size().unstack().fillna(0)
    colors = ['#02C028', '#026014']
    proporcao_counts.plot(kind='bar', stacked=True, figsize=(10, 5), color=colors)

    plt.title('Proporção de Candidatos Masculinos e Femininos por Partido')
    plt.xlabel('Partido')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.legend(title='Gênero')

    for index, value in enumerate(proporcao_counts.values.flatten()):
        plt.text(index // 2, value + 0.5, int(value), ha='center', va='bottom', color='white')

    st.pyplot(plt)



else:
    st.write('Por favor, envie um arquivo CSV.')

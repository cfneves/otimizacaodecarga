import streamlit as st
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga

# Configuração inicial da página
st.set_page_config(page_title="Otimização de Transporte de Carga", layout="wide")
st.title("🚚 Otimização de Transporte de Carga")

# Função para carregar os dados do arquivo CSV
def load_data(file):
    return pd.read_csv(file, sep=";")

# Função de avaliação (fitness) do algoritmo genético
def fitness_function(X, data, max_volume, max_weight):
    selected_items = data.iloc[X.astype(bool), :]
    total_weight = selected_items['PESO'].sum()
    total_volume = selected_items['VOLUME'].sum()
    # Penalizar combinações que excedem o peso ou volume máximo
    if total_weight > max_weight or total_volume > max_volume:
        return -1
    else:
        return -selected_items['VALOR'].sum()  # Minimizar valor negativo para maximizar o valor

# Variável para armazenar os dados do CSV
data = None

# Adicionando o Menu Expansível com Explicação
with st.expander("ℹ️ Como funciona este relatório?", expanded=False):
    st.markdown(
        """
        Este aplicativo realiza uma **Otimização de Transporte de Carga** usando um **algoritmo genético**.
        
        ### Objetivo:
        O objetivo é selecionar itens para transporte de forma que o **valor total** dos itens seja maximizado, 
        enquanto respeita os limites de **peso** e **volume** do veículo.
        
        ### Como funciona:
        - **Carregamento dos Dados**: O usuário carrega um arquivo CSV com informações de peso, volume e valor dos itens.
        - **Configuração do Algoritmo**: É possível ajustar o peso e volume máximos, além de parâmetros do algoritmo genético.
        - **Execução do Algoritmo**: O algoritmo genético seleciona itens que maximizam o valor sem exceder as restrições.
        
        ### Parâmetros do Algoritmo:
        - **Tamanho da População**: Define quantas soluções são geradas em cada iteração.
        - **Probabilidade de Mutação**: Define a taxa de mutação, influenciando a diversidade das soluções.
        - **Número de Iterações**: Define o número máximo de iterações para encontrar uma solução ótima.
        
        Após a execução, o relatório exibe os **itens selecionados** e **métricas** como peso, volume e valor final.
        """
    )

# Layout da interface em colunas com fundo diferenciado e bordas
col1, col2 = st.columns(2)

# Estilo customizado para seções
section_style = """
    <style>
    .st-expander {
        background-color: #f0f2f6;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
    }
    .st-title {
        color: #4CAF50;
    }
    </style>
"""

# Inserir o estilo customizado na página
st.markdown(section_style, unsafe_allow_html=True)

# Expansor para carregar e visualizar dados
with col1.expander("📂 Carregar Dados"):
    uploaded_file = st.file_uploader("Selecione o arquivo CSV", type='csv')
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write("✅ Arquivo carregado com sucesso!")
        # Exibir informações do arquivo carregado
        calculated_button = st.button("📊 Mostrar Estatísticas")
        if calculated_button:
            st.write(data)
            st.write(f"**Quantidade de Itens:** {len(data)}")
            st.write(f"**Peso Total:** {data['PESO'].sum()} kg")
            st.write(f"**Volume Total:** {data['VOLUME'].sum()} m³")
            st.write(f"**Valor Total:** R$ {data['VALOR'].sum():,.2f}")

# Expansor para configurar e rodar o algoritmo genético
with col2.expander("⚙️ Configurações e Execução"):
    if data is not None:
        st.write("### Parâmetros de Restrição:")
        sobra_peso = st.number_input("Sobra de Peso (kg)", min_value=0, value=6000)
        sobra_volume = st.number_input("Sobra de Volume (m³)", min_value=0, value=350)
        iteracao = st.number_input("Quantidade de Iterações", min_value=1, value=10)
        
        st.write("### Configurações do Algoritmo Genético:")
        population_size = st.slider("Tamanho da População", min_value=5, max_value=50, value=10)
        mutation_prob = st.slider("Probabilidade de Mutação", min_value=0.0, max_value=1.0, value=0.1)
        
        process_button = st.button("🚀 Executar Otimização")
        if process_button:
            # Parâmetros do algoritmo
            algorithm_param = {
                'max_num_iteration': iteracao,
                'population_size': population_size,
                'mutation_probability': mutation_prob,
                'elit_ratio': 0.01,
                'crossover_probability': 0.5,
                'parents_portion': 0.3,
                'crossover_type': 'uniform',
                'max_iteration_without_improv': None
            }
            
            varbound = [[0, 1]] * len(data)  # Limites das variáveis para o algoritmo genético
            # Instanciando e executando o modelo
            model = ga(
                function=lambda X: fitness_function(X, data, sobra_volume, sobra_peso),
                dimension=len(data),
                variable_type='bool',
                variable_boundaries=varbound,
                algorithm_parameters=algorithm_param
            )
            with st.spinner("🔄 Processando..."):
                model.run()
            # Resultados e métricas da solução final
            solution = data.iloc[model.output_dict['variable'].astype(bool), :]
            st.write("### 📋 Itens Selecionados:")
            st.write(solution)
            st.write(f"**Quantidade Final de Itens:** {len(solution)}")
            st.write(f"**Peso Final:** {solution['PESO'].sum()} kg")
            st.write(f"**Volume Final:** {solution['VOLUME'].sum()} m³")
            st.write(f"**Valor Total:** R$ {solution['VALOR'].sum():,.2f}")

# --- Rodapé Customizado ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; margin-top: 20px; line-height: 1.2;'>
        <p style='font-size: 16px; font-weight: bold; margin: 0;'>Projeto: Otimização de Transporte de Carga</p>
        <p style='font-size: 14px; margin: 5px 0;'>Desenvolvido por:</p>
        <p style='font-size: 20px; color: #4CAF50; font-weight: bold; margin: 0;'>Cláudio Ferreira Neves</p>
        <p style='font-size: 16px; color: #555; margin: 0;'>Especialista em Análise de Dados, RPA e AI</p>
        <p style='font-size: 14px; margin: 10px 0 5px 0;'>Ferramentas utilizadas: Python, Streamlit, Pandas, Geneticalgorithm</p>
        <p style='font-size: 12px; color: #777; margin: 0;'>© 2024</p>
    </div>
    """,
    unsafe_allow_html=True
)

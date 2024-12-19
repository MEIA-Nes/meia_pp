import pandas as pd
from io import StringIO
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

meis_municipio = pd.read_csv(r'C:\Users\reis_\Desktop\Codes\.vscode\Html\P_P_treino\meia_pp\flaskr\data\meis_municipios.csv')
meis_estado = pd.read_csv(r'C:\Users\reis_\Desktop\Codes\.vscode\Html\P_P_treino\meia_pp\flaskr\data\meis_estados.csv')
meis_regiao = pd.read_csv(r'C:\Users\reis_\Desktop\Codes\.vscode\Html\P_P_treino\meia_pp\flaskr\data\meis_regiao.csv')
idh_municipio = pd.read_csv(r'C:\Users\reis_\Desktop\Codes\.vscode\Html\P_P_treino\meia_pp\flaskr\data\idh_municipio.csv')
idh_estado = pd.read_csv(r'C:\Users\reis_\Desktop\Codes\.vscode\Html\P_P_treino\meia_pp\flaskr\data\idh_estado.csv')

# UTILIZE ESSAS VARIÁVEIS SOMENTE NA FUNÇÃO calc_media_idh_estado, POIS NÃO IRÃO FUNCIONAR NAS DEMAIS FUNÇÕES.
# para calcular do brasil todo:

estados_brasil = list(set(meis_estado['no_uf']))
estados_brasil.sort()

# para calcular da região nordeste:

estados_nordeste = [
    "Alagoas", "Bahia", "Ceará",
    "Maranhão", "Paraíba", "Pernambuco", "Piauí",
    "Rio Grande do Norte", "Sergipe"
]

# para calcular da região norte:

estados_norte = [
    "Acre", "Amapá", "Amazonas", "Pará",
    "Rondônia", "Roraima", "Tocantins"
]

# para calcular da região sudeste:

estados_sudeste = [
    "Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"
]

# para calcular da região centro oeste:

estados_oeste = [
    "Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"
]

municipios_alagoas = list(set(meis_municipio['no_mun']))
municipios_alagoas.sort(key=locale.strxfrm)

# para calcular da região sul:

estados_sul = ['Paraná', 'Santa Catarina', 'Rio Grande do Sul']

def calc_med_idh_estado(value_column, category_column='idh_categoria', year_column='ano', state_column='no_uf', idh_type=None, year=None, states=None, input_file='idh_estado.csv') -> str:
    """
    Calcula a média de uma coluna específica (valores como educação, longevidade, renda ou total)
    filtrando por tipo de IDH, ano e estados, e retorna os resultados em formato de string.

    Args:
        value_column (str): Coluna de valores para calcular a média ('valor').
        category_column (str): Coluna que contém os tipos de IDH. Padrão: 'idh_categoria'.
        year_column (str): Coluna que contém os anos. Padrão: 'ano'.
        state_column (str): Coluna que contém os nomes dos estados. Padrão: 'no_uf'.
        idh_type (str): Tipo específico de IDH a ser filtrado (opcional, ex: 'Educação', 'Renda').
        year (int): Ano específico a ser filtrado (opcional).
        states (list or str): Lista de estados ou um estado específico a ser filtrado (opcional).
        input_file (str): Caminho do arquivo CSV de entrada. Padrão: 'idh_estado.csv'.

    Returns:
        str: Resultado do cálculo em formato de string.
    """
    # Lê o arquivo CSV
    try:
        idh_estado = pd.read_csv(input_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {input_file} não foi encontrado.")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")

    # Verifica se as colunas necessárias estão presentes no DataFrame
    required_columns = [value_column, category_column, year_column, state_column]
    missing_columns = [col for col in required_columns if col not in idh_estado.columns]
    if missing_columns:
        raise ValueError(f"As seguintes colunas estão ausentes no arquivo CSV: {', '.join(missing_columns)}")

    # Filtra pelo tipo de IDH, se especificado
    if idh_type:
        idh_estado = idh_estado[idh_estado[category_column] == idh_type]

    # Filtra pelo ano, se especificado
    if year:
        idh_estado = idh_estado[idh_estado[year_column] == year]

    # Filtra pelos estados, se especificado
    if states:
        if isinstance(states, str):
            states = [states]  # Converte para lista se um único estado for fornecido
        idh_estado = idh_estado[idh_estado[state_column].isin(states)]

    # Calcula a média
    try:
        mean_result = idh_estado.groupby([year_column, category_column])[value_column].mean().reset_index()
    except KeyError as e:
        raise KeyError(f"Erro ao agrupar os dados: {e}")

    # Converte o resultado para string
    result_string = mean_result.to_string(index=False)
    return result_string

def calc_med_idh_municipio(value_column='valor', category_column='idh_categoria', year_column='ano', city_column='no_mun', idh_type=None, year=None, cities=None, input_file='idh_municipio.csv') -> str:
    """
    Calcula a média de uma coluna específica (valores como Educação, Longevidade, Renda ou Total)
    filtrando por tipo de IDH, ano e municípios, e retorna os resultados em formato de string.

    Args:
        value_column (str): Coluna de valores para calcular a média ('valor'). Padrão: 'valor'.
        category_column (str): Coluna que contém os tipos de IDH. Padrão: 'idh_categoria'.
        year_column (str): Coluna que contém os anos. Padrão: 'ano'.
        city_column (str): Coluna que contém os nomes dos municípios. Padrão: 'no_mun'.
        idh_type (str): Tipo específico de IDH a ser filtrado (opcional, ex: 'Educação', 'Renda').
        year (int): Ano específico a ser filtrado (opcional).
        cities (list or str): Lista de municípios ou um município específico a ser filtrado (opcional).
        input_file (str): Caminho do arquivo CSV de entrada. Padrão: 'idh_municipio.csv'.

    Returns:
        str: Resultado do cálculo em formato de string.
    """
    import pandas as pd

    # Lê o arquivo CSV
    try:
        idh_municipio = pd.read_csv(input_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {input_file} não foi encontrado.")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")

    # Verifica se as colunas necessárias estão presentes no DataFrame
    required_columns = [value_column, category_column, year_column, city_column]
    missing_columns = [col for col in required_columns if col not in idh_municipio.columns]
    if missing_columns:
        raise ValueError(f"As seguintes colunas estão ausentes no arquivo CSV: {', '.join(missing_columns)}")

    # Filtra pelo tipo de IDH, se especificado
    if idh_type:
        idh_municipio = idh_municipio[idh_municipio[category_column] == idh_type]

    # Filtra pelo ano, se especificado
    if year:
        idh_municipio = idh_municipio[idh_municipio[year_column] == year]

    # Filtra pelos municípios, se especificado
    if cities:
        if isinstance(cities, str):
            cities = [cities]  # Converte para lista se um único município for fornecido
        idh_municipio = idh_municipio[idh_municipio[city_column].isin(cities)]

    # Calcula a média
    try:
        mean_result = idh_municipio.groupby([year_column, category_column])[value_column].mean().reset_index()
    except KeyError as e:
        raise KeyError(f"Erro ao agrupar os dados: {e}")

    # Converte o resultado para string
    result_string = mean_result.to_string(index=False)
    return result_string

def soma_meis_regiao(ano: int, dados: pd.DataFrame, regioes=None, sum=False) -> str:
    """
    Calcula a soma dos MEIs por região para um ano específico e regiões selecionadas.
    Pode retornar a soma total ou os valores separados por região, dependendo do parâmetro 'sum'.

    Parâmetros:
        ano (int): Ano escolhido pelo usuário.
        dados (DataFrame): DataFrame contendo os dados dos MEIs.
        regioes (list, opcional): Lista de regiões escolhidas pelo usuário. Se None, considera todas as regiões.
        sum (bool, opcional): Se True, retorna a soma total. Se False, mostra valores separados por região.

    Retorna:
        str: Uma string formatada com as regiões e a soma dos MEIs ou o total.
    """
    # Filtrar os dados para o ano escolhido
    dados_filtrados = dados[dados['ano'] == ano]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para o ano {ano}."

    # Filtrar por regiões, se especificado
    if regioes:
        dados_filtrados = dados_filtrados[dados_filtrados['no_reg_geo'].isin(regioes)]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para as regiões {regioes} no ano {ano}."

    # Agrupar por região e somar os valores
    resultado = dados_filtrados.groupby('no_reg_geo')['valor'].sum().reset_index()

    # Se o parâmetro sum for True, somar todas as regiões e retornar o total
    if sum:
        total = resultado['valor'].sum()
        return f"Soma total de MEIs no ano {ano}: {total}"

    # Caso contrário, retornar os valores separados por região
    resultado.columns = ['Regiao', 'Soma_MEIs']
    resultado_str = "\n".join([f"Região: {row['Regiao']}, Soma de MEIs: {row['Soma_MEIs']}" for _, row in resultado.iterrows()])

    return resultado_str

def soma_meis_estados(ano, dados, estados=None, sum=False) -> str:
    """
    Calcula a soma dos MEIs por estado para um ano específico e estados selecionados.
    Pode retornar a soma total ou os valores separados, dependendo do parâmetro 'sum'.

    Parâmetros:
        ano (int): Ano escolhido pelo usuário.
        dados (DataFrame): DataFrame contendo os dados dos MEIs.
        estados (list, opcional): Lista de estados escolhidos pelo usuário. Se None, considera todos os estados.
        sum (bool, opcional): Se True, retorna a soma total. Se False, mostra valores separados por estado.

    Retorna:
        str: Uma string formatada com os estados e a soma dos MEIs para o ano especificado, ou o total.
    """
    # Filtrar os dados para o ano escolhido
    dados_filtrados = dados[dados['ano'] == ano]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para o ano {ano}."

    # Filtrar por estados, se especificado
    if estados:
        dados_filtrados = dados_filtrados[dados_filtrados['no_uf'].isin(estados)]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para os estados {estados} no ano {ano}."

    # Agrupar por estado e somar os valores
    resultado = dados_filtrados.groupby('no_uf')['valor'].sum().reset_index()

    # Se o parâmetro sum for True, somar todos os valores e retornar o total
    if sum:
        total = resultado['valor'].sum()
        return f"Soma total de MEIs no ano {ano}: {total}"

    # Caso contrário, retornar os valores separados por estado
    resultado.columns = ['Estado', 'Soma_MEIs']
    resultado_str = "\n".join([f"Estado: {row['Estado']}, Soma de MEIs: {row['Soma_MEIs']}" for _, row in resultado.iterrows()])

    return resultado_str

def soma_meis_municipios(ano, dados, municipios=None, sum=False) -> str:
    """
    Calcula a soma dos MEIs por município para um ano específico e municípios selecionados.
    Pode retornar a soma total ou os valores separados, dependendo do parâmetro 'sum'.

    Parâmetros:
        ano (int): Ano escolhido pelo usuário.
        dados (DataFrame): DataFrame contendo os dados dos MEIs.
        municipios (list, opcional): Lista de municípios escolhidos pelo usuário. Se None, considera todos os municípios.
        sum (bool, opcional): Se True, retorna a soma total. Se False, mostra valores separados por município.

    Retorna:
        str: Uma string formatada com os municípios e a soma dos MEIs para o ano especificado, ou o total.
    """
    # Filtrar os dados para o ano escolhido
    dados_filtrados = dados[dados['ano'] == ano]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para o ano {ano}."

    # Filtrar por municípios, se especificado
    if municipios:
        dados_filtrados = dados_filtrados[dados_filtrados['no_mun'].isin(municipios)]

    if dados_filtrados.empty:
        return f"Nenhum dado encontrado para os municípios {municipios} no ano {ano}."

    # Agrupar por município e somar os valores
    resultado = dados_filtrados.groupby('no_mun')['valor'].sum().reset_index()

    # Se o parâmetro sum for True, somar todos os valores e retornar o total
    if sum:
        total = resultado['valor'].sum()
        return f"Soma total de MEIs no ano {ano}: {total}"

    # Caso contrário, retornar os valores separados por município
    resultado.columns = ['Município', 'Soma_MEIs']
    resultado_str = "\n".join([f"Município: {row['Município']}, Soma de MEIs: {row['Soma_MEIs']}" for _, row in resultado.iterrows()])

    return resultado_str

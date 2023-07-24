#Criação de duas tabelas: stg_artistas e stg_musica_artista

import pandas as pd

import sys
sys.path.append('../libs')
from fn_database import conectar
from fn_database import executar_consulta
from fn_database import inserir_dados



#Criando tabela
conexao = conectar('bronze_youtube')

query = "SELECT DISTINCT idVideo, artistas AS artista FROM raw_webscrapping_youtube"

artistas = executar_consulta(conexao,query)



# Dividir a coluna 'artista' em várias linhas usando o método split e explode
artistas['artista'] = artistas['artista'].str.split(',')
artistas = artistas.explode('artista')
artistas['artista'] = artistas['artista'].str.strip()  # Remover espaços em branco extras



#Tratando os dados
artistas["artista"] = artistas["artista"].str.replace('("','').str.replace('"','').str.replace("&'","")


artistas = artistas.drop(artistas[artistas['artista'] == '--'].index)
artistas = artistas.drop(artistas[artistas['artista'] == ')'].index)
artistas = artistas.drop(artistas[artistas['artista'] == '''& \''''].index)


# Criar um DataFrame com os valores distintos da coluna "artistas"
artistas_distintos = (pd.DataFrame({'artista': artistas['artista'].unique()}))

# Ordenar o DataFrame por ordem alfabética na coluna "artista"
artistas_distintos.sort_values(by='artista', inplace=True)

# Criar uma coluna "id_artista" com um ID único para cada artista
artistas_distintos['id_artista'] = range(1, len(artistas_distintos) + 1)




# Cria a tabela
conexao = conectar('silver_youtube')
inserir_dados(conexao, 'stg_artistas', [f"`{col}` VARCHAR(1000)" for col in artistas_distintos.columns], dados = artistas_distintos.values.tolist())


query = '''
    SELECT * FROM silver_youtube.stg_artistas
'''
tab_artistas = executar_consulta(conexao,query)


# Mesclar os DataFrames com base na coluna "nomeArtista" e "artista"
df_merged = tab_artistas.merge(artistas, left_on='artista', right_on='artista')

# Remover a coluna "artista" que foi duplicada após a mesclagem
df_merged.drop(columns=['artista'], inplace=True)


#Criando tabela musica_artista
conexao = conectar('silver_youtube')
inserir_dados(conexao, 'stg_faixa_artista', [f"`{col}` VARCHAR(1000)" for col in df_merged.columns], dados = df_merged.values.tolist())

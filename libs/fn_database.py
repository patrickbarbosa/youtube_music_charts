import mysql.connector
import pandas as pd
import numpy as np

#Criar conexão

def conectar(db):
    config = {
        'user': 'patrick',
        'password': 'root',
        'host': '127.0.0.1',
        'database': db
    }
    try:
            conexao = mysql.connector.connect(**config)
            print('Conexão estabelecida com sucesso.')
            return conexao
    except mysql.connector.Error as erro:
            print(f'Erro ao conectar ao MySQL: {erro}')
            return None
        
def inserir_dados(conexao, tabela, colunas, dados=None):
    cursor = conexao.cursor()
    
    # Verifica se a tabela já existe
    cursor.execute(f"SHOW TABLES LIKE '{tabela}'")
    tabela_existe = cursor.fetchone()
    
    if tabela_existe:
        print(f"A tabela '{tabela}' já existe.")
    else:
        # Caso a tabela não exista, cria a tabela
        sql = f"CREATE TABLE {tabela} ({', '.join(colunas)})"
        cursor.execute(sql)
        print(f"Tabela '{tabela}' criada com sucesso.")
        
    if dados:
        # Insere os dados na tabela
        placeholders = ', '.join(['%s'] * len(colunas))
        sql_insert = f"INSERT INTO {tabela} VALUES ({placeholders})"
        cursor.executemany(sql_insert, dados)
        conexao.commit()
        print(f"Dados inseridos na tabela '{tabela}'.")
    
    cursor.close()

def executar_consulta(conexao, consulta):
    try:
        cursor = conexao.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        colunas = cursor.column_names
        cursor.close()
        df = pd.DataFrame(resultado, columns=colunas)
        conexao.commit()
        return df
    except mysql.connector.Error as erro:
        print(f"Erro ao executar consulta SQL: {erro}")
        return None

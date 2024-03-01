import pandas as pd
import sqlite3

# Criando o Conn
conn = sqlite3.connect('sistema.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS atividade (
        Pes INTEGER,
        Cliente text,
        Equipamento text,
        Tecnico text,
        Estagio text,
        Inicio text,
        'Previsão de Término' text,
        Termino text,
        'Manutenção Concluida' INTEGER,
        Observação text)""")

c.execute(""" CREATE TABLE IF NOT EXISTS estagio(
            Estagio text)""")

c.execute("""CREATE TABLE IF NOT EXISTS tecnico(
            Tecnico text,
            Cargo text)""")

df_estagio = pd.read_sql("SELECT * FROM estagio", conn)
df_tecnico = pd.read_sql("SELECT * FROM tecnico", conn)
df_atividade = pd.read_sql("SELECT * FROM atividade", conn)

conn.commit()
conn.close()

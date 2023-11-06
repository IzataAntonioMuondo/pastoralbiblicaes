import sqlite3
conecta_actividade = sqlite3.connect('db/actividade.db', check_same_thread=False)

def create_table_actividade():
    c  = conecta_actividade.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS 
        actividades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data_ini TEXT,
        hora_ini TEXT,
        data_ter TEXT,
        hora_ter TEXT,
        local TEXT, 
        status TEXT,
        imagem TEXT
        
        )
        """
    )
    conecta_actividade.commit()
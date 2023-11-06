import sqlite3
conecta_cursista = sqlite3.connect('db/cursista.db', check_same_thread=False)

def create_table_cursista():
    c = conecta_cursista.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS 
        cursistas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        paroquia TEXT,
        centro TEXT,
        curso TEXT,
        data_ini TEXT,
        data_ter TEXT,
        local TEXT,
        nota TEXT,
        imagem TEXT                    
        )  
        """
    )
    conecta_cursista.commit()
import sqlite3
conecta_cargo = sqlite3.connect('db/cargo.db', check_same_thread = False)

def create_table_cargo():
        c = conecta_cargo.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS 
                cargos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT
                )  
                """)
        
        conecta_cargo.commit()

        print('Tabela cargos criada com sucesso')
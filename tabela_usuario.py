import sqlite3
conn = sqlite3.connect('db/membro.db', check_same_thread = False)

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        membros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data_nasc TEXT,
        genero TEXT,
        morada TEXT,
        contacto TEXT,
        email TEXT,
        moradia TEXT,
        frequenta_escola TEXT,
        estuda_sabado TEXT,
        curso_acad TEXT,
        e_trabalhador TEXT,
        local_trabalho TEXT,
        funcao_trabalho TEXT,
        trabalha_fim_semana TEXT,
        catecumeno TEXT,
        n_f_catequese TEXT,
        tempo_grupo TEXT,
        ano_entrada TEXT,
        tem_cargo TEXT,
        tem_sacramento TEXT,
        tem_promessa TEXT,
        data_promessa TEXT,
        imagem TXT 
        )  
        """)   
    conn.commit()

def create_table_cargo():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        cargos (
        id INTEGER PRIMARY KEY,
        nome TEXT
        )  
        """)    
    conn.commit()
    
def insert_into_cargos():
    c = conn.cursor()
    conn.cursor()
    c.execute('INSERT OR IGNORE INTO cargos (id,nome) VALUES (1, "Coordenador(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (2, "Vice-Coordenador(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (3, "Secretário(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (4, "Vice-secretário(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (5, "Tesoreiro(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (6, "Vice-Tesoreiro(a)")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (7, "Responsável pela infância Bíblica")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (8, "Responsável pela comunicação social")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (9, "Responsável pelo Desporto")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (10, "Responsável pela caridade e convívio")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (11, "Responsável pelos Cursos Bíblicos")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (12, "Responsável pelos materiais")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (13, "Conselheiro")')
    c.execute('INSERT OR IGNORE INTO  cargos (id, nome) VALUES (14, "Outros cargos")')
    conn.commit()
    

    print('Tabela cargos criada com sucesso')

def create_table_associacao_membro_cargo():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        associacao_membro_cargo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        membro_id INTEGER,
        cargo_id INTEGER,
        FOREIGN KEY (membro_id) REFERENCES membros(id),
        FOREIGN KEY (cargo_id) REFERENCES cargos(id)
        )  
        """)
    
    conn.commit()
    
def create_table_sacramento():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        sacramentos (
        id INTEGER PRIMARY KEY,
        nome TEXT
        )  
        """)    
    conn.commit()
    
def insert_into_sacramentos():
    c = conn.cursor()
    conn.cursor()
    c.execute('INSERT OR IGNORE INTO sacramentos (id,nome) VALUES (1, "Baptismo")')
    c.execute('INSERT OR IGNORE INTO  sacramentos (id, nome) VALUES (2, "1ª Comunhão")')
    c.execute('INSERT OR IGNORE INTO  sacramentos (id, nome) VALUES (3, "Crisma")')
    c.execute('INSERT OR IGNORE INTO  sacramentos (id, nome) VALUES (4, "Penitência")')
    c.execute('INSERT OR IGNORE INTO  sacramentos (id, nome) VALUES (5, "Matrimónio")')
    conn.commit()
    
def create_table_associacao_membro_sacramento():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        associacao_membro_sacramento(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        membro_id INTEGER,
        sacramento_id INTEGER,
        FOREIGN KEY (membro_id) REFERENCES membros(id),
        FOREIGN KEY (sacramento_id) REFERENCES sacramentos(id)
        )  
        """)
    
    conn.commit()

def create_table_quota():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        quotas (
        id INTEGER PRIMARY KEY,
        valor INTEGER,
        mes TEXT
        )  
        """)    
    conn.commit()

def insert_into_quotas():
    c = conn.cursor()
    conn.cursor()
    c.execute('INSERT OR IGNORE INTO quotas (id, valor, mes) VALUES (1, 400, "Janeiro")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (2, 400, "Fevereiro")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (3, 400, "Março")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (4, 400, "Abril")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (5, 400, "Maio")')
    c.execute('INSERT OR IGNORE INTO quotas (id, valor, mes) VALUES (6, 400, "Junho")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (7, 400, "Julho")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (8, 400, "Agosto")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (9, 400, "Setembro")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (10, 400, "Outubro")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (11, 400, "Novembro")')
    c.execute('INSERT OR IGNORE INTO  quotas (id, valor, mes) VALUES (12, 400, "Dezembro")')

    conn.commit()

def create_table_associacao_membro_quota():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS 
        associacao_membro_quota(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        membro_id INTEGER,
        quota_id INTEGER,
        FOREIGN KEY (membro_id) REFERENCES membros(id),
        FOREIGN KEY (quota_id) REFERENCES quotas(id)
        )  
        """)
    conn.commit()

def create_table_leitura():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS
              leituras(
              data DATE PRIMARY KEY,
              tempo_liturgico TEXT,
              pri_leitura TEXT,
              salmo TEXT,
              seg_leitura TEXT,
              evangelho TEXT
            )""")
    conn.commit()

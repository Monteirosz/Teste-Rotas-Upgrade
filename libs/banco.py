import sqlite3

def criar_tabela():
    con = sqlite3.connect('informacoes.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS INFOS')

    comando = '''CREATE TABLE INFOS (
        USUARIO TEXT,
        SENHA TEXT,
        EMAIL TEXT,
        TELEFONE TEXT
        )'''

    cur.execute(comando)
    con.close()

def view_tabela():
    con = sqlite3.connect('informacoes.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM INFOS")
    dados = cur.fetchall()
    con.close()
    return dados

def validar_login(user, senha):
    con = sqlite3.connect('informacoes.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM INFOS WHERE USUARIO = ? AND SENHA = ?', (user, senha))
    resultado = cur.fetchone()
    con.close()
    return resultado

def inserir_usuario(user, senha, email, telefone):
    con = sqlite3.connect('informacoes.db')
    cur = con.cursor()
    cur.execute('INSERT INTO INFOS (USUARIO, SENHA, EMAIL, TELEFONE) values(?,?,?,?)', (user, senha, email, telefone))
    con.commit()
    con.close()

criar_tabela()
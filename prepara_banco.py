import sqlite3
from wrap_connection import transact

print('Conectando ...')

conn = sqlite3.connect("jogoteca.db")

def make_connection():
    conn = sqlite3.connect("jogoteca.db")
    return conn

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `jogoteca;")
#conn.commit()

criar_tabelas = '''
    CREATE TABLE `jogo` (
      id int(11) NOT NULL PRIMARY KEY,
      nome varchar(50) NOT NULL,
      categoria varchar(40) NOT NULL,
      console varchar(20) NOT NULL,
    )
    CREATE TABLE `usuario` (
      id varchar(8) NOT NULL,
      nome` varchar(20) NOT NULL,
      senha` varchar(8) NOT NULL,
      PRIMARY KEY (id)
    )'''

@transact(make_connection)
def criar_db():
    conn.cursor().execute(criar_tabelas)
    conn.commit()
    
criar_db()

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO jogoteca.usuario (id, nome, senha) VALUES (?, ?, ?)',
      [
            ('luan', 'Luan Marques', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogoteca.jogo (nome, categoria, console) VALUES (?, ?, ?)',
      [
            ('God of War 4', 'Acao', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estrategia', '3DS'),
      ])

cursor.execute('select * from jogoteca.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()

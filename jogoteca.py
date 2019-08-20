from flask import Flask, render_template, request, redirect, session, flash, url_for
#from dao import JogoDao
import sqlite3

app = Flask(__name__)
app.secret_key = 'sessao'

database = sqlite3.connect('jogoteca.db') #banco 
cursor = database.cursor() # cursor de manipulação do banco
jogo_dao = cursor

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

lista1 = {
    'jogo':'alex'
}
class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

lista = [] 
cursor.execute('select * from jogo')
#jogos = []
for jogo in cursor.fetchall():
    lista.append(Jogo(jogo[1],jogo[2],jogo[3]))


@app.route('/')
def index():
    
    return render_template("lista.html", titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima= url_for('novo'))) #chama a função login e passa a proxima pagina como parametro
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome'] #name de nome no formulario
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')# variavel que foi definida no redirect
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuarios = [] 
    cursor.execute('select * from usuario')
    #jogos = []
    for user in cursor.fetchall():
        usuarios.append(Jogo(user[1],user[2]))
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id #salva a sessão do usuario em um cookie
            flash(usuario.nome + ' logou com sucesso!') #mostra uma msg rapida pro usuario
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, Tente Novamente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum Usuario Logado!')
    return redirect(url_for('index')) #o url_for é a função da rota que vai ser chamada

app.run(debug=True)
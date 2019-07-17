from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'sessao'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
lista = [jogo1, jogo2, jogo3]

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
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')# variavel que foi definida no redirect
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'mestra' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario'] #salva a sessão do usuario em um cookie
        flash(request.form['usuario'] + ' logou com sucesso!') #mostra uma msg rapida pro usuario
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
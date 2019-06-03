from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

ficheiro = sqlite3.connect('utilizadores.db')
c = ficheiro.cursor()


def criar_tabela():
    c.execute('CREATE TABLE IF NOT EXISTS utilizador (utilizador text, passe text)')

criar_tabela()

def gravar_dados():
    c.execute("INSERT INTO utilizador VALUES ('chouriças', 'cachorro')")
    ficheiro.commit()

gravar_dados()
ficheiro.close()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

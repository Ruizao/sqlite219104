from flask import Flask, render_template, request

app = Flask(__name__)


def gravar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (usr text, pwd text)")
    db.execute("INSERT INTO usr VALUES (?, ?)", (v1, v2))
    ficheiro.commit()
    ficheiro.close()
    return

def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET pwd = ? WHERE usr = ?", (v2, v1))
    ficheiro.commit()
    ficheiro.close()
    return


def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ?", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor

def log(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ? and pwd = ?", (v1, v2))
    valor = db.fetchone()
    ficheiro.close()
    return valor

def eliminar(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE usr = ?", (v1,))
    ficheiro.commit()
    ficheiro.close()
    return

@app.route('/newpass', methods=['POST', 'GET'])
def newpass():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if not existe(v1):
            erro = 'O utilizador não existe '
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
            erro = 'A palavra passe foi alterada com sucesso.'
    return render_template('newpass.html', erro=erro)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if existe(v1):
            erro = 'O utilizador não existe '
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2)
            erro = 'O Utilizador  foi registado com sucesso.'
    return render_template('registro.html', erro=erro)

@app.route('/login', methods=['POST', 'GET'])
def login():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O utilizador não existe '
        elif not log(v1, v2):
            erro = 'A palavra passe está incorreta.'
        else:
            gravar(v1, v2)
            erro = 'Bem-vindo.'
    return render_template('login.html', erro=erro)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O utilizador não existe '
        elif not log(v1, v2):
            erro = 'A palavra passe está incorreta.'
        else:
            eliminar(v1)
            erro = 'Conta eliminada com sucesso'
    return render_template('delete.html', erro=erro)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, flash
from model.controler_usuario import Usuario
from model.controler_mensagem import Mensagem

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura' 

@app.route("/")
def index():
    if "nome" not in session:
        return redirect("/login")

    mensagens = Mensagem.recuperar_mensagens()
    nome_usuario = session["nome"]
    return render_template("index.html", mensagens=mensagens, nome_usuario=nome_usuario)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/post/login", methods=["POST"])
def login_post():
    login = request.form["login"]
    senha = request.form["senha"]

    if Usuario.validar_login(login, senha):
     
        conexao_bd = Conexao.criar_conexao()
        cursor = conexao_bd.cursor(dictionary=True)
        cursor.execute("SELECT nome FROM tb_usuarios WHERE login = %s", (login,))
        usuario = cursor.fetchone()
        cursor.close()
        conexao_bd.close()

        session["login"] = login
        session["nome"] = usuario["nome"]
        return redirect("/")
    else:
        flash("Login ou senha incorretos!")
        return redirect("/login")

@app.route("/post/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    login = request.form["login"]
    senha = request.form["senha"]

    if Usuario.cadastrar(login, senha, nome):
        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect("/login")
    else:
        flash("Este nome de usuário já está em uso.")
        return redirect("/login")

@app.route("/post/cadastrar_mensagem", methods=["POST"])
def cadastrar_mensagem():
    if "nome" not in session:
        return redirect("/login")

    nome = session["nome"]
    comentario = request.form["comentario"]
    Mensagem.cadastrar_mensagem(nome, comentario)
    return redirect("/")

@app.route("/post/curtir_mensagem", methods=["POST"])
def curtir_mensagem():
    cod = request.form["id_mensagem"]
    Mensagem.curtir_mensagem(cod)
    return redirect("/")

@app.route("/post/descurtir_mensagem", methods=["POST"])
def descurtir_mensagem():
    cod = request.form["id_mensagem"]
    Mensagem.descurtir_mensagem(cod)
    return redirect("/")

@app.route("/post/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    cod = request.form["id_mensagem"]
    Mensagem.excluir_mensagem(cod)
    return redirect("/")

@app.route("/post/sair")
def sair():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)

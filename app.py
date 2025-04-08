from flask import Flask, render_template, request, redirect, session, flash
from model.controler_usuario import Usuario
from model.controler_mensagem import Mensagem

app = Flask(__name__)
app.secret_key = 'minha_chave_super_secreta'  # Altere isso por segurança

# Página principal protegida
@app.route("/")
def index():
    if "usuario" not in session:
        return redirect("/login")

    mensagens = Mensagem.recuperar_mensagens()
    nome_usuario = session["usuario"]  # <- pega o nome
    return render_template("index.html", mensagens=mensagens, nome_usuario=nome_usuario)

# Página de login/cadastro
@app.route("/login")
def tela_login():
    return render_template("login.html")

# Rota para login
@app.route("/post/login", methods=["POST"])
def login():
    login = request.form["login"]
    senha = request.form["senha"]

    if Usuario.validar_login(login, senha):
        session["usuario"] = login
        return redirect("/")
    else:
        flash("Login ou senha incorretos.")
        return redirect("/login")

# Rota para cadastro
@app.route("/post/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    login = request.form["login"]
    senha = request.form["senha"]

    if Usuario.cadastrar(login, senha, nome):
        flash("Cadastro realizado com sucesso!")
        return redirect("/login")
    else:
        flash("Usuário já existe.")
        return redirect("/login")

# Rota para logout
@app.route("/post/sair")
def sair():
    session.clear()
    return redirect("/login")

# Rota para cadastrar comentário
@app.route("/post/cadastrar_mensagem", methods=["POST"])
def cadastrar_mensagem():
    if "usuario" not in session:
        return redirect("/login")

    comentario = request.form["comentario"]
    nome = session["usuario"]
    Mensagem.cadastrar_mensagem(nome, comentario)
    return redirect("/")


@app.route("/post/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    if "usuario" not in session:
        return redirect("/login")

    cod_comentario = request.form["id_mensagem"]
    Mensagem.excluir_mensagem(cod_comentario)
    return redirect("/")

@app.route("/post/curtir_mensagem", methods=["POST"])
def curtir_mensagem():
    if "usuario" not in session:
        return redirect("/login")

    cod_comentario = request.form["id_mensagem"]
    Mensagem.curtir_mensagem(cod_comentario)
    return redirect("/")

# Descurtir comentário
@app.route("/post/descurtir_mensagem", methods=["POST"])
def descurtir_mensagem():
    if "usuario" not in session:
        return redirect("/login")

    cod_comentario = request.form["id_mensagem"]
    Mensagem.descurtir_mensagem(cod_comentario)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

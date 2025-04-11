from flask import Flask, render_template, request, redirect, session, flash
from model.controler_usuario import Usuario
from model.controler_mensagem import Mensagem
import os
from data.conexao import Conexao

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrao_segura')

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
    login = request.form.get("login")
    senha = request.form.get("senha")

    if not login or not senha:
        flash("Preencha todos os campos!", "error")
        return redirect("/login")

    try:
        if Usuario.validar_login(login, senha):
            conexao = Conexao.criar_conexao()
            if conexao is None:
                flash("Erro ao conectar ao banco de dados", "error")
                return redirect("/login")
                
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT nome FROM tb_usuarios WHERE login = %s", (login,))
            usuario = cursor.fetchone()
            cursor.close()
            conexao.close()

            if usuario:
                session["login"] = login
                session["nome"] = usuario["nome"]
                return redirect("/")
            else:
                flash("Erro ao recuperar dados do usuário", "error")
        else:
            flash("Login ou senha incorretos!", "error")
    except Exception as e:
        flash(f"Erro interno: {str(e)}", "error")
    
    return redirect("/login")

@app.route("/post/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    login = request.form.get("login")
    senha = request.form.get("senha")

    if not all([nome, login, senha]):
        flash("Preencha todos os campos!", "error")
        return redirect("/login")

    try:
        if Usuario.cadastrar(login, senha, nome):
            flash("Cadastro realizado com sucesso! Faça login.", "success")
        else:
            flash("Este nome de usuário já está em uso.", "error")
    except Exception as e:
        flash(f"Erro ao cadastrar: {str(e)}", "error")
    
    return redirect("/login")

@app.route("/post/cadastrar_mensagem", methods=["POST"])
def cadastrar_mensagem():
    if "nome" not in session:
        return redirect("/login")

    try:
        nome = session["nome"]
        comentario = request.form.get("comentario")
        if not comentario:
            flash("O comentário não pode estar vazio!", "error")
            return redirect("/")
            
        Mensagem.cadastrar_mensagem(nome, comentario)
    except Exception as e:
        flash(f"Erro ao postar mensagem: {str(e)}", "error")
    
    return redirect("/")

@app.route("/post/curtir_mensagem", methods=["POST"])
def curtir_mensagem():
    if "nome" not in session:
        return redirect("/login")

    try:
        cod = request.form.get("id_mensagem")
        if cod:
            Mensagem.curtir_mensagem(cod)
    except Exception as e:
        flash(f"Erro ao curtir: {str(e)}", "error")
    
    return redirect("/")

@app.route("/post/descurtir_mensagem", methods=["POST"])
def descurtir_mensagem():
    if "nome" not in session:
        return redirect("/login")

    try:
        cod = request.form.get("id_mensagem")
        if cod:
            Mensagem.descurtir_mensagem(cod)
    except Exception as e:
        flash(f"Erro ao descurtir: {str(e)}", "error")
    
    return redirect("/")

@app.route("/post/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    if "nome" not in session:
        return redirect("/login")

    try:
        cod = request.form.get("id_mensagem")
        if cod:
            Mensagem.excluir_mensagem(cod)
    except Exception as e:
        flash(f"Erro ao excluir: {str(e)}", "error")
    
    return redirect("/")

@app.route("/post/sair")
def sair():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
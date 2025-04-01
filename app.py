from flask import Flask, render_template, request, redirect, session, flash
from data.conexao import Conexao
from model.controler_usuario import Usuario
from model.controler_mensagem import Mensagem

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Para mensagens flash

@app.route("/mensagens")
def pagina_mensagem():
    if 'user' not in session:
        return redirect("/")  # Redireciona para a página de login se não estiver autenticado
    
    mensagens = Mensagem.recuperar_mensagens()
    return render_template("index.html", mensagens=mensagens)

@app.route("/post/cadastrar_mensagem", methods=["POST"])
def post_mensagem():
    if 'user' not in session:
        return redirect("/")  # Redireciona para a página de login se não estiver autenticado

    nome = session.get('user')
    comentario = request.form.get("comentario")

    if not comentario:
        return "Erro: Comentário não pode estar vazio!", 400

    Mensagem.cadastrar_mensagem(nome, comentario)
    
    return redirect("/mensagens")

@app.route("/post/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    cod_comentario = request.form.get("id_mensagem")

    if cod_comentario:
        Mensagem.excluir_mensagem(cod_comentario)

    return redirect("/mensagens")

@app.route("/post/curtir_mensagem", methods=["POST"])
def curtir_mensagem():
    cod_comentario = request.form.get("id_mensagem")

    if cod_comentario:
        Mensagem.curtir_mensagem(cod_comentario)

    return redirect("/mensagens")

@app.route("/post/descurtir_mensagem", methods=["POST"])
def descurtir_mensagem():
    cod_comentario = request.form.get("id_mensagem")

    if cod_comentario:
        Mensagem.descurtir_mensagem(cod_comentario)

    return redirect("/mensagens")

@app.route("/post/login", methods=["POST"])
def login():
    login_usuario = request.form.get("login")
    senha = request.form.get("senha")

    if not login_usuario or not senha:
        flash("Todos os campos são obrigatórios!")
        return redirect("/")

    if Usuario.validar_login(login_usuario, senha):
        session['user'] = login_usuario
        return redirect("/mensagens")
    else:
        flash("Usuário ou senha inválidos!")
        return redirect("/")

@app.route("/post/cadastrar", methods=["POST"])
def cadastrar_usuario():
    nome = request.form.get("nome")
    login = request.form.get("login")
    senha = request.form.get("senha")

    if not nome or not login or not senha:
        flash("Todos os campos são obrigatórios!")
        return redirect("/")

    if Usuario.verificar_usuario_existe(login):
        flash("Usuário já existe!")
        return redirect("/")

    Usuario.cadastrar(login, senha, nome)
    
    flash("Cadastro realizado com sucesso!")
    return redirect("/")

@app.route("/post/sair", methods=["GET"])
def sair():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect("/")  # Redireciona para a página de login

@app.route("/")
def pagina_principal():
    if 'user' in session:
        return redirect("/mensagens")  # Se já estiver logado, vai para a página de mensagens
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)

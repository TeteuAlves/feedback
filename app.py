from flask import Flask, render_template, request, redirect
from data.conexao import Conexao
from model.controler_mensagem import Mensagem

app = Flask(__name__)

@app.route("/")
def pagina_principal():
    mensagens = Mensagem.recuperar_mensagens()
    return render_template("index.html", mensagens=mensagens)

@app.route("/post/cadastrar_mensagem", methods=["POST"])
def post_mensagem():
    nome = request.form.get("user")
    comentario = request.form.get("comentario")

    if not nome or not comentario:
        return "Erro: Usuário e comentário não podem estar vazios!", 400

    Mensagem.cadastrar_mensagem(nome, comentario)
    
    return redirect("/")

@app.route("/post/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    cod_comentario = request.form.get("id_mensagem")

    if cod_comentario:
        Mensagem.excluir_mensagem(cod_comentario)

    return redirect("/")

@app.route("/post/curtir_mensagem", methods=["POST"])
def curtir_mensagem():
    cod_comentario = request.form.get("id_mensagem")

    if cod_comentario:
        Mensagem.curtir_mensagem(cod_comentario)

    return redirect("/")

app.run(debug=True)

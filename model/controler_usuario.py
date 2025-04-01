import hashlib
from data.conexao import Conexao

class Usuario:
    @staticmethod
    def validar_login(login, senha):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor(dictionary=True)

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        sql = "SELECT * FROM tb_usuarios WHERE login = %s AND senha = %s"
        cursor.execute(sql, (login, senha_hash))
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        return usuario is not None

    @staticmethod
    def verificar_usuario_existe(login):
        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        sql = "SELECT COUNT(*) FROM tb_usuarios WHERE login = %s"
        cursor.execute(sql, (login,))
        existe = cursor.fetchone()[0] > 0

        cursor.close()
        conexao.close()

        return existe

    @staticmethod
    def cadastrar(login, senha, nome):
        if Usuario.verificar_usuario_existe(login):
            return False  # Retorna False se o usuário já existir

        conexao = Conexao.criar_conexao()
        cursor = conexao.cursor()

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        sql = "INSERT INTO tb_usuarios (login, senha, nome) VALUES (%s, %s, %s)"
        valores = (login, senha_hash, nome)

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()
        
        return True  # Retorna True se o cadastro for bem-sucedido

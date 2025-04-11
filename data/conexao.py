# conexao.py - Versão corrigida
import mysql.connector

class Conexao:
    @staticmethod
    def criar_conexao():
        conexao = mysql.connector.connect(
            host="bdgodofredo-alexstocco-93db.b.alvencloud.com",
            port=27974,
            user="3ds",
            password="banana",
            database="db_feedback"
        )
        return conexao
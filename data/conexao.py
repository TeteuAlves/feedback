import mysql.connector

class Conexao:

    def criar_conexao():
        conexao = mysql.connector.connect(
            host = "bdgodofredo-alexsstocco-93db.b.aivencloud.com", port = 27974, user = "3ds", password = "banana", database = "db_feedback"
        )
        return conexao

    


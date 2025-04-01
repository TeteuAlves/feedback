import mysql.connector

class Conexao:

    def criar_conexao():
        conexao = mysql.connector.connect(
            host = "10.110.131.18", port = 3306, user = "3ds", password = "banana", database = "db_feedback"
        )
        return conexao

    


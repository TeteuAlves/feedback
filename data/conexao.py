import mysql.connector

# class Conexao:
    # def criar_conexao():
    #         #criando a conexão
    #         conexao = mysql.connector.connect(host = "bdgodofredo-alexstocco-93db.b.aivencloud.com",
    #                                         port = 27974,
    #                                         user = "3ds",
    #                                         password = "banana",
    #                                         database = "db_feedback")
class Conexao:
    #Criando a conexão localmente
    def criar_conexao():
        conexao = mysql.connector.connect(host = "localhost",
                                            port = 3306,
                                            user = "3ds",
                                            password = "banana",
                                            database = "db_feedback")
        return conexao
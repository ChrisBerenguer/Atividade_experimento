import sqlite3

# Importação do sqlite3 para salvar dados de entrada de forma permanente

class Model(object):
    def __init__(self, *args):
        self.conexao = sqlite3.connect("pyc.db")
        self.cursor = self.conexao.cursor()
        self.create_model()


    def create_model(self, *args):
        sqlquery = ("create table if not exists file("
                    " cod_file integer primary key autoincrement,"
                    " description varchar(500),"
                    " name_file varchar(500) not null,"
                    " file blob not null,"
                    " date_create date default current_timestamp)")
        self.cursor.execute(sqlquery)
        self.conexao.commit()


    def search_file(self, *args):
        sqlquery = ("select f.cod_file, f.description, f.name_file from file f")
        self.cursor.execute(sqlquery)
        return self.cursor.fetchall()

    def save_file(self, description, name_file, file):
        sqlquery = ("insert into file"
                    " (description, name_file, file) values (?,?,?)")

        sqlargs = (description, name_file, sqlite3.Binary(file))
        self.cursor.execute(sqlquery,sqlargs)
        self.conexao.commit()

    def delete_file(self,codigo):
        sqlquery = ("delete from file where cod_file = ?")
        sqlargs = [codigo]

        self.cursor.execute(sqlquery, sqlargs)
        self.conexao.commit()


    def search_file_id(self, codigo):
        sqlquery = ("select f.name_file, f.file from file f"
                    "where f.cod_file = ?")
        sqlargs = [codigo]
        self.cursor.execute(sqlquery, sqlargs)
        return self.cursor.fetchall()


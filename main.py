import gi
import os
import zlib

gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from model import Model

builder = Gtk.Builder()
builder.add_from_file("Atv_Interface.glade")


class App(Model):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args,**kwargs)
        self.comecar_ui()
        self.renderer_model(self.search_file())

    def comecar_ui(self):
        self.chooser_button = builder.get_object("chooser_button")
        self.entry_descricao = builder.get_object("entry_descricao")
        self.grade_arquivos = builder.get_object("grade_arquivos")
        self.list_arquivos = builder.get_object("list_arquivos")
        self.atividade_janela = builder.get_object("atividade_janela")
        self.atividade_janela.show_all()


    def on_atividade_janela_destroy(self, *args):   # Comando que encerra a aplicação
        Gtk.main_quit()

    # Renderizador do modelo de dados na grade
    def renderer_model(self, model):
        try:
            self.list_arquivos.clear()
            if model:
                # print(model)

                for arquivos in model:
                    self.list_arquivos.append(arquivos)

        except Exception as ex:
            print("Erro %s" % ex)

    # Adicionar o arquivo no Banco de Dados sqlite3
    def on_bt_adicionar_clicked(self, *args):
        try:
            caminho_arquivo = self.chooser_button.get_filename()
            descricao = self.entry_descricao.get_text()
            arquivo = zlib.compress(open(caminho_arquivo, "rb").read(), 9)   # Compressão do arquivo com Zlib
            nome_arquivo = os.path.basename(caminho_arquivo)
            # print(nome_arquivo)
            self.save_file(descricao, nome_arquivo, arquivo)
            self.renderer_model(self.search_file())
        except Exception as ex:
            print("Erro %s" % ex)
            self.conexao.rollback()

    # Adiciona ao banco de dados ao selecionar registro na grade
    def on_grade_arquivos_cursor_changed(self, *args):
        try:
            self.cod_arquivo = self.select_code(args[0].get_selection())


        except Exception as ex:
            print("Erro: %s" % ex)

    # Retornar o conteúdo da primeira cel
    def select_code(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            return model[treeiter][0]


    # Deleta arquivos do banco de dados
    def on_bt_remover_clicked(self,*args):
        try:
            self.delete_file(self.cod_arquivo)
            self.renderer_model(self.search_file())
        except Exception as ex:
            print("Erro: %s" % ex)
            self.conexao.rollback()


    def on_bt_abrir_clicked(self, *args):
        try:
            arquivo = self.search_file_id(self.cod_arquivo)
            if arquivo:
                path = os.path.join("/temp/", arquivo[0][0])
                with open(path, "wb") as file:
                    file.write(zlib.decompress(arquivo[0][1]))
                os.system("xdg-open" + path)

        except Exception as ex:
            print("Erro: %s" % ex)


if __name__ == "__main__":
    builder.connect_signals(App())
    Gtk.main()



'''Builder = Gtk.Builder()
Builder.add_from_file("Atv_Interface.glade")
Builder.connect_signals(Manipulador())
window = Builder.get_object('tela_principal')
window.show_all()
Gtk.main()'''





from Model import Usuario as u
from Controller import usuario as uc


class UsuarioViewer:

    def create_usuario_element(usuario: u.Usuario) -> str:
        return (f"<a href=\"/detalhe_despesa?id=1\" class=\"item\">"
            f"<span class=\"id\">{_esc(usuario.id)} </span>"
            f"<span class=\"nome\">{_esc(usuario.nome)} </span>"
            f"<span class=\"tipo\">{_esc(usuario.tipo)} </span>"
            f"<span class=\"email\">{_esc(usuario.email)} </span>"
            f"<span class=\"status\">{_esc(usuario.status)} </span>"
            f"</a>")

    def call_listar(self):
        lista = ""

        with open("View_and_Interface/views/lista_user.html", "r",
                      encoding="utf-8") as f:
            print("Leu Pagina")
            conteudo = f.read()
            for usuario in uc.UsuarioController.listar():
                print('Interou com user -> ${usuario.name}')
                newElement = self.create_usuario_element(usuario)
                lista.concat(newElement)
            
            conteudo.replace("<!-- Dados -->", lista)

        return conteudo

    def call_menu():
        with open("View_and_Interface/views/menu_user.html", "rb") as f:
            conteudo = f.read()

        return conteudo
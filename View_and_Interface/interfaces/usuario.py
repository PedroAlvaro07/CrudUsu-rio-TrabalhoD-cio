from html import escape
from Model import Usuario as u
from Controller import usuario as uc


def _esc(v):
    return escape("" if v is None else str(v))


class UsuarioViewer:

    @staticmethod
    def create_usuario_element(usuario: u.Usuario) -> str:
        return (f"<a href=\"/detalhe_despesa?id=1\" class=\"item\">"
                f"<span class=\"id\">{_esc(usuario.id)} </span>"
                f"<span class=\"nome\">{_esc(usuario.nome)} </span>"
                f"<span class=\"tipo\">{_esc(usuario.tipo)} </span>"
                f"<span class=\"email\">{_esc(usuario.email)} </span>"
                f"<span class=\"status\">{_esc(usuario.status)} </span>"
                f"</a>")

    @staticmethod
    def call_listar() -> str:
        lista = ""

        with open("View_and_Interface/views/lista_user.html", "r",
                  encoding="utf-8") as f:
            print("Leu Pagina")
            conteudo = f.read()

            controller = uc.UsuarioController()
            users = controller.listar()
            # controller may return nested list in some implementations; normalize
            if isinstance(users, list) and len(users) == 1 and isinstance(users[0], list):
                users = users[0]

            for usuario in users:
                print(f'Iterou com user -> {getattr(usuario, "nome", None)}')
                newElement = UsuarioViewer.create_usuario_element(usuario)
                lista += newElement

            conteudo = conteudo.replace("<!-- Dados -->", lista)

        return conteudo

    @staticmethod
    def call_menu():
        with open("View_and_Interface/views/menu_user.html", "rb") as f:
            conteudo = f.read()

        return conteudo
from html import escape
from Model import Usuario as u
from Controller import usuario as uc


def _esc(v):
    return escape("" if v is None else str(v))


class UsuarioViewer:

    @staticmethod
    def create_usuario_element(usuario: u.Usuario) -> str:

        return (
            "<tr>"
            f"<td>{_esc(usuario.id)}</td>"
            f"<td>{_esc(usuario.nome)}</td>"
            f"<td>{_esc(usuario.tipo)}</td>"
            f"<td>{_esc(usuario.email)}</td>"
            f"<td>{_esc(usuario.status)}</td>"
            "</tr>"
        )

    @staticmethod
    def call_listar(controller) -> str:
        lista = ""

        with open("View_and_Interface/views/lista_user.html", "r",
                  encoding="utf-8") as f:
            print("Leu Pagina")
            conteudo = f.read()

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
    def call_cadastrar() -> str:
        lista = ""

        with open("View_and_Interface/views/cadastro_user.html", "r",
                  encoding="utf-8") as f:
            conteudo = f.read()

            conteudo = conteudo.replace("<!-- Dados -->", lista)

        return conteudo

    @staticmethod
    def call_menu():
        with open("View_and_Interface/views/menu_user.html", "rb") as f:
            conteudo = f.read()

        return conteudo
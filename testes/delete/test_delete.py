import pytest

import sys
import os

# Adicionando o path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from View_and_Interface import view
from Controller import usuario as uc
from Model import Usuario as u

lista_usuarios = [
    u.Usuario(
        id=1,
        nome="João",
        matricula="ESOFT01-C",
        tipo="ALUNO",
        email="joao@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=2,
        nome="Ana",
        matricula="ESOFT01-A",
        tipo="ALUNO",
        email="ana@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
    u.Usuario(
        id=3,
        nome="Jose",
        matricula="ESOFT01-B",
        tipo="ALUNO",
        email="jose@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="SUSPENSO",
    ),
    u.Usuario(
        id=4,
        nome="Mariana",
        matricula="ESOFT01-B",
        tipo="ALUNO",
        email="mariana@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=5,
        nome="Carlos",
        matricula="PROF01",
        tipo="PROFESSOR",
        email="carlos@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=6,
        nome="Beatriz",
        matricula="PROF02",
        tipo="PROFESSOR",
        email="beatriz@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=7,
        nome="Fernando",
        matricula="PROF03",
        tipo="PROFESSOR",
        email="fernando@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
    u.Usuario(
        id=8,
        nome="Luciana",
        matricula="PROF04",
        tipo="PROFESSOR",
        email="luciana@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=9,
        nome="Paulo",
        matricula="FUNC01",
        tipo="FUNCIONARIO",
        email="paulo@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="ATIVO",
    ),
    u.Usuario(
        id=10,
        nome="Sofia",
        matricula="FUNC01",
        tipo="FUNCIONARIO",
        email="sofia@example.com",
        ativoDeRegistro="2025-01-15T10:30:00Z",
        status="INATIVO",
    ),
]

userController = uc.UsuarioController(usuarios = lista_usuarios)

@pytest.mark.parametrize("user_id", [
    (4),
    (1),
    (2),
])
def test_delete_existendo_um_cliente_id(client, user_id):
    item_id, _ = created_user
    result = userController.delete(user_id)
    assert result is True
    assert userController.obter_por_id(user_id) is None

def test_delete_nonexistent_user_by_id(client):
    assert userController.delete(9999) is False

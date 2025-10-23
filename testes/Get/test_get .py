import pytest

from datetime import datetime

def test_criacao_usuario_basico():
    usuario = User(
        id=1,
        nome="Pedro",
        matricula="ABC123",
        tipo="ALUNO",
        email="pedro@email.com"
    )
    assert usuario.id == 1
    assert usuario.nome == "Pedro"
    assert usuario.matricula == "ABC123"
    assert usuario.tipo == "ALUNO"
    assert usuario.email == "pedro@email.com"
    assert usuario.status == "ATIVO"
    # Verifica se a data está no formato ISO
    assert isinstance(usuario.ativoDeRegistro, str)
    datetime.fromisoformat(usuario.ativoDeRegistro)

def test_usuario_inativo():
    usuario = User(2, "Maria", "XYZ999", "PROFESSOR", status="INATIVO")
    assert usuario.status == "INATIVO"
    assert not usuario.is_ativo()


def test_get_user_existing():
    result = get_user(1)
    assert result == {"id": 1, "nome": "João", "matricula:": "ESOFT", "tipo": "Aluno", 
                      "email": "jp@fromTheSouth", "ativoDeRegistro": "Ativo" }

def test_get_user_not_found():
    result = get_user(99)
    assert result is None

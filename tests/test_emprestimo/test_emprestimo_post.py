import uuid
import pytest
from datetime import datetime, timedelta

from controler import EmprestimoController
from Model import Emprestimo as e

emprestimoController = EmprestimoController()

def make_payload(**overrides):
    base = {
        "id": uuid.uuid4().int & (1<<16)-1,
        "usuario": 1,
        "livro": 101,
        "loan_date": datetime.now().isoformat(),
        "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "data_devolucao_real": None
    }
    base.update(overrides)
    return base


def create_emprestimo(dados: dict):
    return emprestimoController.criar(dados)


def test_create_emprestimo_success():
    payload = make_payload()
    resp = create_emprestimo(payload)
    assert resp.usuario == payload["usuario"]
    assert resp.livro == payload["livro"]
    assert resp.loan_date == payload["loan_date"]
    assert resp.due_date == payload["data_devolucao_prevista"]


@pytest.mark.parametrize("dias,valid", [
    (5, True),
    (0, False),
    (-3, False),
])
def test_validacao_data_devolucao_prevista(dias, valid):
    data_emprestimo = datetime.now()
    data_prevista = data_emprestimo + timedelta(days=dias)
    payload = make_payload(
        data_emprestimo=data_emprestimo.isoformat(),
        data_devolucao_prevista=data_prevista.isoformat()
    )
    try:
        resp = create_emprestimo(payload)
        if valid:
            assert resp.get_data_devolucao_prevista() == data_prevista.isoformat()
        else:
            pytest.fail("Should have raised ValueError for invalid date")
    except ValueError as e:
        assert not valid
        assert "Data de devolução deve ser posterior à data de empréstimo" in str(e)


@pytest.mark.parametrize("missing_field", [
    "usuario", "livro", "data_emprestimo", "data_devolucao_prevista"
])
def test_falta_de_campo(missing_field):
    payload = make_payload()
    payload.pop(missing_field, None)

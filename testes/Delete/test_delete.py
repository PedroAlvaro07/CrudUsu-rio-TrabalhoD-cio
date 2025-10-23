import pytest

from testes.store import InMemoryStore


@pytest.fixture
def store():
    return InMemoryStore()


def test_delete_existing_item(store):
    # Arrange: criar um item
    payload = {"id" : 1,"name": "Alice", "matricula" : "230694372" , "tipo" : "ALUNO","email": "alice@example.com", "ativoDoRegistro" : "23/10/2025", "status" : "ATIVO"}
    item_id = store.create(payload)

    # Act: deletar o item
    result = store.delete(item_id)

    # Assert: delete retorna True e leitura posterior é None
    assert result is True
    assert store.read(item_id) is None


def test_delete_nonexistent_item(store):
    # Act: tentar deletar um id que não existe
    result = store.delete(9999)

    # Assert: deve retornar False e não lançar exceção
    assert result is False

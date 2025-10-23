import uuid
import pytest
from datetime import datetime, timezone, timedelta

# Helper to build valid payloads with optional overrides
def make_payload(**overrides):
    base = {
        "nome": "Fulano de Tal",
        "matricula": f"M{uuid.uuid4().hex[:8]}",
        "tipo": "ALUNO",
        "email": f"user.{uuid.uuid4().hex[:8]}@example.com",
        "ativoDeRegistro": datetime.now(timezone.utc).isoformat(),
        "status": "ATIVO",
    }
    base.update(overrides)
    return base

def create_user(client, payload):
    return client.post("/users", json=payload)

def assert_validation_error(response):
    assert response.status_code in (400, 422), "expected validation error (400/422)"

def assert_conflict_error(response):
    assert response.status_code in (409, 400), "expected conflict (409) or validation (400)"

def assert_created(response):
    assert response.status_code in (200, 201), "expected created (200/201)"
    try:
        data = response.get_json()
    except Exception:
        data = None
    assert data, "response must contain JSON body"
    assert "matricula" in data and "email" in data, "created object must include identifiers"


def test_create_user_success(client):
    payload = make_payload()
    resp = create_user(client, payload)
    assert_created(resp)
    data = resp.get_json()
    assert data["nome"] == payload["nome"]
    assert data["matricula"] == payload["matricula"]
    assert data["tipo"] == payload["tipo"]
    assert data["email"] == payload["email"]
    assert data["status"] == payload["status"]


@pytest.mark.parametrize("length,valid", [
    (0, True),    # allowed according to provided spec (0...100)
    (1, True),
    (100, True),
    (101, False),
])
def test_nome_length_validation(client, length, valid):
    nome = "A" * length
    payload = make_payload(nome=nome)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


@pytest.mark.parametrize("matricula,valid", [
    ("1234", False),                 # too short (<5)
    ("1" * 5, True),                 # boundary 5
    ("1" * 20, True),                # boundary 20
    ("1" * 21, False),               # too long (>20)
])
def test_matricula_length_validation(client, matricula, valid):
    payload = make_payload(matricula=matricula)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


def test_matricula_uniqueness(client):
    unique = f"M{uuid.uuid4().hex[:8]}"
    p1 = make_payload(matricula=unique)
    p2 = make_payload(matricula=unique)
    r1 = create_user(client, p1)
    assert_created(r1)
    r2 = create_user(client, p2)
    assert_conflict_error(r2)


@pytest.mark.parametrize("tipo,valid", [
    ("ALUNO", True),
    ("PROFESSOR", True),
    ("FUNCIONARIO", True),
    ("STAGIARE", False),
    ("", False),
    (None, False),
])
def test_tipo_enum_validation(client, tipo, valid):
    payload = make_payload(tipo=tipo)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


@pytest.mark.parametrize("email,valid", [
    ("valid.email@example.com", True),
    ("invalid-email", False),
    ("no-at-sign.com", False),
    ("@missing-local.com", False),
])
def test_email_format_validation(client, email, valid):
    payload = make_payload(email=email)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


def test_email_uniqueness(client):
    email = f"user.{uuid.uuid4().hex[:8]}@example.com"
    p1 = make_payload(email=email)
    p2 = make_payload(email=email)
    r1 = create_user(client, p1)
    assert_created(r1)
    r2 = create_user(client, p2)
    assert_conflict_error(r2)


@pytest.mark.parametrize("date_str,valid", [
    (datetime.now(timezone.utc).isoformat(), True),
    ("2020-01-01", True),                 # date-only ISO 8601 is acceptable
    ("01-01-2020", False),
    ("2020/01/01", False),
    ("not-a-date", False),
    ("", False),
])
def test_ativoDeRegistro_iso8601_validation(client, date_str, valid):
    payload = make_payload(ativoDeRegistro=date_str)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


@pytest.mark.parametrize("status,valid", [
    ("ATIVO", True),
    ("INATIVO", True),
    ("SUSPENSO", True),
    ("DEMITIDO", False),
    ("", False),
    (None, False),
])
def test_status_enum_validation(client, status, valid):
    payload = make_payload(status=status)
    resp = create_user(client, payload)
    if valid:
        assert_created(resp)
    else:
        assert_validation_error(resp)


@pytest.mark.parametrize("missing_field", [
    "nome", "matricula", "tipo", "email", "ativoDeRegistro", "status"
])
def test_missing_required_fields(client, missing_field):
    payload = make_payload()
    payload.pop(missing_field, None)
    resp = create_user(client, payload)
    assert_validation_error(resp)
"""
Exemplo de arquivo de teste para o módulo Usuario

Este é um exemplo de como estruturar os testes.
Os alunos devem criar seus próprios testes seguindo TDD.

Execute com: pytest tests/test_usuario_exemplo.py
"""

import pytest
# from Model.Usuario import Usuario  # Descomentar quando implementar


class TestUsuarioExemplo:
    """
    Classe de exemplo para testes do módulo Usuario
    
    Os alunos devem:
    1. Descomentar os imports
    2. Implementar a classe Usuario
    3. Fazer os testes passarem
    4. Adicionar mais testes
    """
    
    def test_exemplo_placeholder(self):
        """
        Teste de placeholder para garantir que pytest funciona
        
        REMOVER este teste quando implementar os testes reais
        """
        assert True
    
    # DESCOMENTAR E IMPLEMENTAR:
    
    # def test_criar_usuario_valido(self):
    #     """Testa criação de usuário válido"""
    #     usuario = Usuario("2021001", "João Silva", "aluno")
    #     assert usuario.matricula == "2021001"
    #     assert usuario.nome == "João Silva"
    #     assert usuario.tipo == "aluno"
    
    # def test_usuario_sem_matricula(self):
    #     """Testa que não é possível criar usuário sem matrícula"""
    #     with pytest.raises(ValueError, match="Matrícula.*obrigatória"):
    #         Usuario("", "João Silva", "aluno")
    
    # def test_nome_muito_curto(self):
    #     """Testa validação de tamanho mínimo do nome"""
    #     with pytest.raises(ValueError, match="Nome.*3 caracteres"):
    #         Usuario("2021001", "Jo", "aluno")
    
    # def test_tipo_usuario_invalido(self):
    #     """Testa que tipo de usuário deve ser válido"""
    #     with pytest.raises(ValueError, match="Tipo.*inválido"):
    #         Usuario("2021001", "João Silva", "admin")
    
    # def test_email_valido_opcional(self):
    #     """Testa que email é opcional mas deve ser válido se fornecido"""
    #     usuario = Usuario("2021001", "João Silva", "aluno", "joao@email.com")
    #     assert usuario.email == "joao@email.com"
    
    # def test_usuario_to_dict(self):
    #     """Testa serialização do usuário para dicionário"""
    #     usuario = Usuario("2021001", "João Silva", "aluno")
    #     dados = usuario.to_dict()
    #     
    #     assert "id" in dados
    #     assert "matricula" in dados
    #     assert "nome" in dados
    #     assert "tipo" in dados


# Adicionar mais 4 testes unitários e 5 testes de contrato

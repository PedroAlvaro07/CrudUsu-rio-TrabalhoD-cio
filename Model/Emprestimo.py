"""
Model: Emprestimo
Módulo 3 - Empréstimo e Devolução

Este arquivo deve ser implementado pelos alunos usando TDD (Test Driven Development).

Requisitos:
- Classe Emprestimo com atributos: id, usuario_id, livro_id, data_emprestimo, prazo_devolucao, data_devolucao, status
- Validações:
  * usuario_id deve existir
  * livro_id deve existir e estar disponível
  * data_emprestimo não pode ser futura
  * prazo_devolucao deve ser posterior à data_emprestimo
  * status deve ser 'ativo', 'devolvido' ou 'atrasado'
- Métodos:
  * verificar_disponibilidade_livro()
  * calcular_dias_atraso()
  * registrar_devolucao()
  * verificar_atraso()

Exemplos de testes a implementar:
- test_criar_emprestimo_valido()
- test_emprestar_livro_indisponivel()
- test_calcular_dias_atraso()
- test_registrar_devolucao()
- test_verificar_atraso()
- test_prazo_devolucao_invalido()
"""

class Emprestimo:
    """
    Classe que representa um empréstimo de livro
    
    TODO: Implementar usando TDD
    """
    pass

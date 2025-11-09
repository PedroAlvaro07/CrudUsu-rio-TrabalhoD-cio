"""
Model: Relatorio
Módulo 4 - Relatórios

Este arquivo deve ser implementado pelos alunos usando TDD (Test Driven Development).

Requisitos:
- Classe Relatorio com métodos para gerar relatórios e estatísticas
- Métodos:
  * livros_mais_emprestados(limite=10)
  * usuarios_mais_ativos(limite=10)
  * livros_por_categoria()
  * taxa_ocupacao()
  * emprestimos_por_periodo(data_inicio, data_fim)
  * total_emprestimos_ativos()
  * emprestimos_em_atraso()

Exemplos de testes a implementar:
- test_livros_mais_emprestados()
- test_usuarios_mais_ativos()
- test_calcular_taxa_ocupacao()
- test_filtrar_emprestimos_por_periodo()
- test_contar_emprestimos_ativos()
- test_listar_emprestimos_atrasados()
"""

from Model import Livro as l
from Model import Usuario as u
from Model import Emprestimo as e

class Relatorio:
    """
    Classe responsável por gerar relatórios e estatísticas do sistema.
    Espera receber listas de objetos (usuarios, livros, emprestimos)
    vindos de outros módulos do projeto.
    """

    def __init__(self, usuarios, livros, emprestimos):
        self.usuarios = usuarios or []
        self.livros = livros or []
        self.emprestimos = emprestimos or []

    def get_livros(self) -> list[l.Livro]:
        return self.livros

    def get_usuarios(self) -> list[u.Usuario]:
        return self.usuarios
    
    def get_emprestimos(self) -> list[e.Emprestimo]:
        return self.emprestimos

    def set_livros(self, livros):
        self.livros = livros or []

    def set_usuarios(self, usuarios):
        self.usuarios = usuarios or []

    def set_emprestimos(self, emprestimos):
        self.emprestimos = emprestimos or []


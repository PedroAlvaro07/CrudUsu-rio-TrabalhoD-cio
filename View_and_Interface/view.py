from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
from controler import UsuarioController
from controler import LivroController
from controler import RelatorioController
from controler import EmprestimoController
from datetime import datetime
from collections import Counter

usuario = UsuarioController()
livro = LivroController()
emprestimo = EmprestimoController()
relatorio = RelatorioController(usuario.listar(), livro.listar_livros(), emprestimo.listar())

def _esc(v):
    """Escapa valores HTML para evitar XSS"""
    return escape("" if v is None else str(v))


class BibliotecaView(BaseHTTPRequestHandler):
    """
    Servidor HTTP que controla todas as telas do SGBU via Python.
    Os alunos devem implementar as classes em Model/ e integrar via controler.py
    """

    def do_GET(self):
        """Trata requisicoes GET - exibe paginas"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Redireciona raiz para cadastro
        if path == '/':
            self.send_response(302)
            self.send_header("Location", "/cadastro")
            self.end_headers()
        
        # Modulo 1: Cadastro de Usuarios
        elif path == '/cadastro':
            self.render_cadastro()
        elif path == '/cadastro/novo':
            self.render_form_usuario()
        elif path in '/cadastro/editar?matricula=':
            self.render_form_usuario_edit()
        
        # Modulo 2: Catalogo de Livros
        elif path == '/livros':
            self.render_livros()
        elif path == '/livros/novo':
            self.render_form_livro()
        elif path == '/autores':
            self.render_autores()
        
        # Modulo 3: Emprestimos
        elif path == '/emprestimos':
            self.render_emprestimos()
        elif path == '/emprestimos/novo':
            self.render_form_emprestimo()
        
        # Modulo 4: Relatorios
        elif path == '/relatorios':
            self.render_relatorios()
        elif path == '/relatorios/usuarios-ativos':
            self.render_usuarios_ativos()
        
        else:
            self.send_error(404, "Pagina nao encontrada")

    def do_POST(self):
        """Trata requisicoes POST - processa formularios"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(body)
        print(params)
        
        # Converte para dict simples
        data = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
        
        if path == '/cadastro/salvar':
            self.processar_usuario(data)
        elif path == '/cadastro/editar':
            self.editar_usuario(data)
        elif path == '/livros/salvar':
            self.processar_livro(data)
        elif path == '/emprestimos/salvar':
            self.processar_emprestimo(data)
        else:
            self.send_error(404)

    # ========== RENDERIZACAO - MODULO 1: USUARIOS ==========
    
    def render_cadastro(self):
        """Renderiza pagina de listagem de usuarios"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = """
            <div class="actions">
                <h2>Lista de Usuarios</h2>
                <a href="/cadastro/novo" class="btn btn-primary">+ Novo Usuario</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                        <th>Nome</th>
                        <th>Matricula</th>
                        <th>Tipo</th>
                        <th>Email</th>
                        <th>Data de Registro</th>
                        <th>Status</th>
                        </tr>
                    </thead>
                    <tbody> 
        """
        
        usuarios = usuario.listar()
        
        for u in usuarios:
            data_obj = datetime.fromisoformat(u.ativoDeRegistro.replace("Z", "+00:00"))
            data_formatada = data_obj.strftime("%d-%m-%Y")

            conteudo += f'''
                <tr onclick="window.location.href='/cadastro/editar?matricula={u.id}'" style="cursor: pointer;">
                    <td>{ u.nome }</td>
                    <td>{ u.matricula }</td>
                    <td>{ u.tipo }</td>
                    <td>{ u.email }</td>
                    <td>{ data_formatada }</td>
                    <td>{ u.status }</td>
                </tr>
            '''
        conteudo += """ 
                    </tbody>
                </table>
            </div> """


        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)

    def render_form_usuario_edit(self):
        """Renderiza formulario de cadastro de usuario"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()

        id = self.path.split('=')[1]
        usuarioEdit = usuario.obter_por_id(int(id))
        
        conteudo = f'''
            <div class="form-container">
            <h2>Editar Usuario</h2>
            <form action="/cadastro/salvar" method="post">
                <div class="form-group">
                <label>Matricula *</label>
                <input type="text" name="matricula" value="{_esc(usuarioEdit.matricula)}" required>
                </div>
                <div class="form-group">
                <label>Nome Completo *</label>
                <input type="text" name="nome" value="{_esc(usuarioEdit.nome)}" required>
                </div>
                <div class="form-group">
                <label>Tipo de Usuario *</label>
                <select name="tipo" required>
                    <option value="">Selecione...</option>
                    <option value="ALUNO" {"selected" if usuarioEdit.tipo == "ALUNO" else ""}>Aluno</option>
                    <option value="PROFESSOR" {"selected" if usuarioEdit.tipo == "PROFESSOR" else ""}>Professor</option>
                    <option value="FUNCIONARIO" {"selected" if usuarioEdit.tipo == "FUNCIONARIO" else ""}>Funcionario</option>
                </select>
                </div>
                <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" value="{_esc(usuarioEdit.email if usuarioEdit.email else '')}">
                </div>
                <div class="form-group">
                <label>Status do Usuario *</label>
                <select name="status" required>
                    <option value="">Selecione...</option>
                    <option value="ATIVO" {"selected" if usuarioEdit.status == "ATIVO" else ""}>Ativo</option>
                    <option value="INATIVO" {"selected" if usuarioEdit.status == "INATIVO" else ""}>Inativo</option>
                    <option value="SUSPENSO" {"selected" if usuarioEdit.status == "SUSPENSO" else ""}>Suspenso</option>
                </select>
                </div>
                <div class="form-group">
                <label>Data de registro</label>
                <input type="date" name="ativoDeRegistro" value="{_esc(usuarioEdit.ativoDeRegistro[:10] if usuarioEdit.ativoDeRegistro else '')}">
                </div>
                <div class="form-actions">
                <a href="/editar" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                <button type="submit" class="btn btn-primary">Salvar</button>
                </div>
            </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_usuario(self):
        """Renderiza formulario de cadastro de usuario"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="form-container">
                <h2>Novo Usuario</h2>
                <form action="/cadastro/salvar" method="post">
                    <div class="form-group">
                        <label>Matricula *</label>
                        <input type="text" name="matricula" required>
                    </div>
                    <div class="form-group">
                        <label>Nome Completo *</label>
                        <input type="text" name="nome" required>
                    </div>
                    <div class="form-group">
                        <label>Tipo de Usuario *</label>
                        <select name="tipo" required>
                            <option value="">Selecione...</option>
                            <option value="ALUNO">Aluno</option>
                            <option value="PROFESSOR">Professor</option>
                            <option value="FUNCIONARIO">Funcionario</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email">
                    </div>
                    <div class="form-group">
                        <label>Status do Usuario *</label>
                        <select name="status" required>
                            <option value="">Selecione...</option>
                            <option value="ATIVO">Ativo</option>
                            <option value="INATIVO">Inativo</option>
                            <option value="SUSPENSO">Suspenso</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Data de registro</label>
                        <input type="date" name="ativoDeRegistro">
                    </div>
                    <div class="form-actions">
                        <a href="/cadastro" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Salvar</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)

    def editar_usuario(self, data):
        """Processa formulario de usuario (exibe dados mas nao salva)"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            usuario.atualizar(data)

        except (ValueError) as ve:
            mensagem = f'''
                <div class="alert alert-error">
                    <strong>Erro ao salvar usuario:</strong> {_esc(str(ve))}
                </div>
                <a href="/cadastro/novo" class="btn btn-primary">Voltar para formulario</a>
            '''
            
            html = html.replace('<!--CONTEUDO-->', mensagem)
            self.send_html(html)
            return
        

        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>Matricula:</strong> {_esc(data.get('matricula'))}</p>
                <p><strong>Nome:</strong> {_esc(data.get('nome'))}</p>
                <p><strong>Status:</strong> {_esc(data.get('status'))}</p>
                <p><strong>Tipo:</strong> {_esc(data.get('tipo'))}</p>
                <p><strong>Data de Registro:</strong> {_esc(data.get('ativoDeRegistro'))}</p>
                <p><strong>Email:</strong> {_esc(data.get('email', 'Nao informado'))}</p>
            </div>
            <br>
            <a href="/cadastro" class="btn btn-primary">Voltar para lista</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    def processar_usuario(self, data):
        """Processa formulario de usuario (exibe dados mas nao salva)"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            usuario.criar(data)

        except (ValueError) as ve:
            mensagem = f'''
                <div class="alert alert-error">
                    <strong>Erro ao salvar usuario:</strong> {_esc(str(ve))}
                </div>
                <a href="/cadastro/novo" class="btn btn-primary">Voltar para formulario</a>
            '''
            
            html = html.replace('<!--CONTEUDO-->', mensagem)
            self.send_html(html)
            return
        

        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>Matricula:</strong> {_esc(data.get('matricula'))}</p>
                <p><strong>Nome:</strong> {_esc(data.get('nome'))}</p>
                <p><strong>Status:</strong> {_esc(data.get('status'))}</p>
                <p><strong>Tipo:</strong> {_esc(data.get('tipo'))}</p>
                <p><strong>Data de Registro:</strong> {_esc(data.get('ativoDeRegistro'))}</p>
                <p><strong>Email:</strong> {_esc(data.get('email', 'Nao informado'))}</p>
            </div>
            <br>
            <a href="/cadastro" class="btn btn-primary">Voltar para lista</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 2: LIVROS ==========
    
    def render_livros(self):
        """Renderiza pagina de catalogo de livros"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="tabs">
                <a href="/livros" class="tab active">Livros</a>
                <a href="/autores" class="tab">Autores</a>
            </div>
            <div class="actions">
                <h2>Lista de Livros</h2>
                <a href="/livros/novo" class="btn btn-primary">+ Novo Livro</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Titulo</th>
                            <th>Autor</th>
                            <th>ISBN</th>
                        </tr>
                    </thead>
                    <tbody> 
        '''
        
        livros = livro.listar_livros()
        
        for l in livros:
            conteudo += f'''
                <tr>
                    <td>{ l.titulo }</td>
                    <td>{ l.autor }</td>
                    <td>{ l.isbn }</td>
                </tr>
            '''
        conteudo += """ 
                    </tbody>
                </table>
            </div> """

        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_autores(self):
        """Renderiza pagina de autores"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="tabs">
                <a href="/livros" class="tab">Livros</a>
                <a href="/autores" class="tab active">Autores</a>
            </div>
            <div class="actions" style="justify-content: space-between; display: flex;">
                <h2>Lista de Autores dos livros da base</h2>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Nome do autor</th>
                        </tr>
                    </thead>
                    <tbody> 
        '''
        
        autores = livro.listar_autores()
        id = 0
        
        for a in autores:
            id += 1
            conteudo += f'''
                <tr>
                    <td>{ id }</td>
                    <td>{ a }</td>
                </tr>
            '''
        conteudo += """ 
                    </tbody>
                </table>
            </div> """
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_livro(self):
        """Renderiza formulario de cadastro de livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="form-container">
                <h2>Novo Livro</h2>
                <form action="/livros/salvar" method="post">
                    <div class="form-group">
                        <label for="titulo">Título:</label>
                        <input type="text" id="titulo" name="titulo" required>
                    </div>
                    <div class="form-group">
                        <label for="autor">Autor:</label>
                        <input type="text" id="autor" name="autor" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="isbn">ISBN:</label>
                        <input type="text" id="isbn" name="isbn" required>
                    </div>
                    <div class="form-actions">
                        <a href="/livros" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Salvar</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_livro(self, data):
        """Processa formulario de livro (exibe dados mas nao salva)"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            livro.criar_livro(data)

        except (ValueError) as ve:
            mensagem = f'''
                <div class="alert alert-error">
                    <strong>Erro ao salvar livro:</strong> {_esc(str(ve))}
                </div>
                <a href="/livros/novo" class="btn btn-primary">Voltar para formulario</a>
            '''
            
            html = html.replace('<!--CONTEUDO-->', mensagem)
            self.send_html(html)
            return

        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>ISBN:</strong> {_esc(data.get('isbn'))}</p>
                <p><strong>Titulo:</strong> {_esc(data.get('titulo'))}</p>
                <p><strong>Autor:</strong> {_esc(data.get('autor'))}</p>
            </div>
            <br>
            <a href="/livros" class="btn btn-primary">Voltar para catalogo</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 3: EMPRESTIMOS ==========
    
    def render_emprestimos(self):
        """Renderiza pagina de emprestimos"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        emprestimos_ativos = len([emp for emp in emprestimo.listar() if emp.status == "ATIVO"])
        emprestimos_atrasados = len([emp for emp in emprestimo.listar() if emp.esta_em_atraso()])
        devolvidos_hoje = len([emp for emp in emprestimo.listar() if emp.return_date and emp.return_date.date() == datetime.now().date()])

        conteudo = f'''
            <div class="stats">
                <div class="stat-card">
                    <h3>Emprestimos Ativos</h3>
                    <div class="value">{ emprestimos_ativos }</div>
                </div>
                <div class="stat-card">
                    <h3>Emprestimos em Atraso</h3>
                    <div class="value">{ emprestimos_atrasados }</div>
                </div>
                <div class="stat-card">
                    <h3>Devolvidos Hoje</h3>
                    <div class="value">{ emprestimos_atrasados }</div>
                </div>
            </div>
            <div class="actions" style="justify-content: space-between; display: flex;">
                <h2>Lista de Emprestimos</h2>
                <a href="/emprestimos/novo" class="btn btn-primary">+ Novo Emprestimo</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Nome do responsável</th>
                            <th>Titulo do livro</th>
                        </tr>
                    </thead>
                    <tbody> 
        '''
        
        emprestimos = emprestimo.listar()
        
        for e in emprestimos:
            conteudo += f'''
                <tr>
                    <td>{ e.usuario.nome }</td>
                    <td>{ e.livro.titulo }</td>
                </tr>
            '''
            
        conteudo += """ 
                    </tbody>
                </table>
            </div> """

        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_emprestimo(self):
        """Renderiza formulario de novo emprestimo"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        


        conteudo = f'''
            <div class="form-container">
                <h2>Novo Emprestimo</h2>
                <form action="/emprestimos/salvar" method="post">
                    <div class="form-group">
                        <label>Usuario *</label>
                        <select name="usuario_id" required>
                            <option value="">Selecione um usuario...</option>
                            {''.join([f'<option value="{_esc(u.matricula)}">{_esc(u.nome)} ({_esc(u.matricula)})</option>' for u in usuario.listar()])}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Livro *</label>
                        <select name="livro_id" required>
                            <option value="">Selecione um livro...</option>
                            {''.join([f'<option value="{_esc(l.isbn)}">{_esc(l.titulo)} ({_esc(l.isbn)})</option>' for l in livro.listar_livros()])}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Data do Emprestimo *</label>
                        <input type="date" name="data_emprestimo" required>
                    </div>
                    <div class="form-group">
                        <label>Prazo de Devolucao *</label>
                        <input type="date" name="prazo_devolucao" required>
                    </div>
                    <div class="form-actions">
                        <a href="/emprestimos" class="btn btn-secondary" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Salvar</button>
                    </div>
                </form>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_emprestimo(self, data):
        """Processa formulario de emprestimo (exibe dados mas nao salva)"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        mensagem = f'''
            <div class="alert alert-success">
                Dados recebidos com sucesso!
            </div>
            <div class="alert alert-error">
                <strong>Funcionalidade nao implementada:</strong> Os alunos devem implementar
                a classe Emprestimo em Model/Emprestimo.py e integrar via controler.py
            </div>
            <div style="background: white; padding: 20px; border-radius: 12px;">
                <h3>Dados enviados:</h3>
                <p><strong>Usuario ID:</strong> {_esc(data.get('usuario_id'))}</p>
                <p><strong>Livro ID:</strong> {_esc(data.get('livro_id'))}</p>
                <p><strong>Data Emprestimo:</strong> {_esc(data.get('data_emprestimo'))}</p>
                <p><strong>Prazo Devolucao:</strong> {_esc(data.get('prazo_devolucao'))}</p>
            </div>
            <br>
            <a href="/emprestimos" class="btn btn-primary">Voltar para lista</a>
        '''
        
        html = html.replace('<!--CONTEUDO-->', mensagem)
        self.send_html(html)

    # ========== RENDERIZACAO - MODULO 4: RELATORIOS ==========
    
    def render_relatorios(self):
        """Renderiza pagina de relatorios"""
        with open("View_and_Interface/relatorios.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        relatorio.carregar_dados(
            usuarios=usuario.listar(),
            livros=livro.listar_livros(),
            emprestimos=emprestimo.listar() 
        )

        conteudo = '''
            <div class="report-cards">
                <div class="report-card">
                    <div class="icon">Stats</div>
                    <h3>Visao Geral</h3>
                    <p>Dashboard com estatisticas gerais</p>
                </div>
                <div class="report-card">
                    <div class="icon">Books</div>
                    <h3>Livros Mais Emprestados</h3>
                    <p>Ranking de popularidade</p>
                </div>
                <a href="/relatorios/usuarios-ativos" class="report-card-link">
                    <div class="report-card">
                        <div class="icon">Users</div>
                        <h3>Usuarios Mais Ativos</h3>
                        <p>Top usuarios por emprestimos</p>
                    </div>
                </a>
                <div class="report-card">
                    <div class="icon">Chart</div>
                    <h3>Taxa de Ocupacao</h3>
                    <p>Percentual de livros emprestados</p>
                </div>
            </div>
            <div class="empty-state">
                <h3>Funcionalidade nao implementada</h3>
                <p>Os alunos devem implementar a classe <strong>Relatorio</strong> em <code>Model/Relatorio.py</code></p>
                <p>e integrar via <code>controler.py</code> para gerar relatorios.</p>
                <p><strong>Nota:</strong> Este modulo depende de TODOS os outros modulos!</p>
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)

    def render_usuarios_ativos(self):
        """Renderiza pagina de usuarios mais ativos"""
        with open("View_and_Interface/relatorios.html", "r", encoding="utf-8") as f:
            html = f.read()

        relatorio.carregar_dados(
            usuarios=usuario.listar(),
            livros=livro.listar_livros(),
            emprestimos=emprestimo.listar()
        )

        usuarios = relatorio.usuarios_mais_ativos()

        print(usuarios)

        conteudo = '''
            <div class="actions">
                <h2>Lista de Usuarios mais ativos</h2>
                <a href="/cadastro/novo" class="btn btn-primary">+ Novo Usuario</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Nome do usuário</th>
                            <th>Quantidade de Livros emprestados</th>
                        </tr>
                    </thead>
                    <tbody> 
        '''
        
        for u in usuarios:
            conteudo += f'''
                <tr>
                    <td>{ u['usuario'].nome }</td>
                    <td>{ u['quantidade'] }</td>
                </tr>
            '''
        conteudo += """ 
                    </tbody>
                </table>
            </div> 
            <a href="/relatorios" class="btn btn-primary">Voltar para menu de relatórios</a>
            <a href="/emprestimos/novo" class="btn btn-primary">Voltar para formulario de emprestimo</a>
        """
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)

    # ========== METODOS AUXILIARES ==========
    
    def send_html(self, html):
        """Envia resposta HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        """Log das requisicoes HTTP"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Inicia o servidor HTTP na porta especificada"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibliotecaView)
    print(f"Servidor SGBU iniciado em http://localhost:{port}")
    print(f"Acesse: http://localhost:{port}/cadastro")
    print(f"Pressione Ctrl+C para encerrar")
    print()
    print("ATENCAO: As funcionalidades de CRUD ainda nao estao implementadas.")
    print("   Os alunos devem implementar as classes em Model/ usando TDD.")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()

class Usuario:
    def __init__(self, nome, matricula, tipo, email, ativoDeRegistro, status):
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo
        self.email = email
        self.ativoDeRegistro = ativoDeRegistro
        self.status = status

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_matricula(self):
        return self.matricula

    def set_matricula(self, matricula):
        self.matricula = matricula

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_ativoDeRegistro(self):
        return self.ativoDeRegistro

    def set_ativoDeRegistro(self, ativoDeRegistro):
        self.ativoDeRegistro = ativoDeRegistro

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
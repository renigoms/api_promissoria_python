class Cliente:
    def __init__(self, nome_completo=None, cpf=None, email=None, telefone=None, id=None, ativo=None):
        self.id = id
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.ativo = ativo

    def to_dict(self):
        return dict(id=self.id,
                    nome_completo=self.nome_completo,
                    cpf=self.cpf,
                    email=self.email,
                    telefone=self.telefone,
                    ativo=self.ativo)

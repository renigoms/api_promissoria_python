class Cliente:
    def __init__(self, nome_completo=None, cpf=None, email=None, telefone=None, id=None):
        self._id = id
        self._nome_completo = nome_completo
        self._cpf = cpf
        self._email = email
        self._telefone = telefone

    def __str__(self):
        return ("Cliente: id={},nome_completo={},cpf={},email={},"
                "telefone={}").format(self._id, self._nome_completo, self._cpf, self._email, self._telefone) \
            if self._id is not None \
            else "Cliente: nome_completo={},cpf={},email={},telefone={}".format(self._nome_completo, self._cpf, self._email, self._telefone)
    
    @property
    def id(self):
        return self._id

    @property
    def nome_completo(self):
        return self._nome_completo

    @property
    def cpf(self):
        return self._cpf

    @property
    def email(self):
        return self._email

    @property
    def telefone(self):
        return self._telefone

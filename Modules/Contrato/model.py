class Contrato:
    def __init__(self, id=None, id_cliente=None, id_produto=None, num_parcelas=0,
                 qnt_produto=1, valor=None, descricao=None, data_criacao=None, parcelas_definidas=None):
        self._id = id
        self._id_cliente = id_cliente
        self._id_produto = id_produto
        self._num_parcelas = num_parcelas
        self._qnt_produto = qnt_produto
        self._valor = valor
        self._descricao = descricao
        self._data_criacao = data_criacao.strftime('%d-%m-%Y') if data_criacao is not None else data_criacao
        self._parcelas_definidas = parcelas_definidas

    def __str__(self):
        return ("Contrato: id={}, id_cliente={}, "
                "id_produto={}, num_parcelas={}, "
                "qnt_produto={}, valor={}, descricao={}, "
                "data_criacao={}, parcelas_definidas={})"
                ).format(
                    self._id, self._id_cliente,
                    self._id_produto, self._num_parcelas,
                    self._qnt_produto, self._valor,
                    self._descricao, self._data_criacao,
                    self._parcelas_definidas
                    ) \
            if self._id is not None \
            else ("Contrato: id_cliente={}, "
                  "id_produto={}, num_parcelas={}, "
                  "qnt_produto={}, valor={}, descricao={}, "
                  "data_criacao={}, parcelas_definidas={})"
                  ).format(
                        self._id_cliente, self._id_produto, self._num_parcelas,
                        self._qnt_produto, self._valor, self._descricao,
                        self._data_criacao, self._parcelas_definidas
                    )
                  
    @property
    def id(self):
        return self._id

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def id_produto(self):
        return self._id_produto

    @property
    def num_parcelas(self):
         return self._num_parcelas

    @property
    def qnt_produto(self):
        return self._qnt_produto

    @property
    def valor(self):
        return self._valor

    @property
    def descricao(self):
        return self._descricao

    @property
    def data_criacao(self):
        return self._data_criacao

    @property
    def parcelas_definidas(self):
        return self._parcelas_definidas



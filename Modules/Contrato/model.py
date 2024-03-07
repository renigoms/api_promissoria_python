class Contrato:
    def __init__(self, id: int = None, id_cliente: int = None, itens_produto: list = None,
                 num_parcelas: int = None, valor: float = None, descricao: str = None,
                 data_criacao=None, parcelas_definidas: bool = None, ativo: bool = None):
        self.id = id
        self.id_cliente = id_cliente
        self.itens_produto = itens_produto
        self.num_parcelas = num_parcelas
        self.valor = valor
        self.descricao = descricao
        self.data_criacao = data_criacao.strftime('%d-%m-%Y') if data_criacao is not None else data_criacao
        self.parcelas_definidas = parcelas_definidas
        self.ativo = ativo

    def to_dict(self):
        return dict(id=self.id,
                    id_cliente=self.id_cliente,
                    num_parcelas=self.num_parcelas,
                    valor=float(self.valor),
                    descricao=self.descricao,
                    data_criacao=self.data_criacao,
                    parcelas_definidas=self.parcelas_definidas,
                    ativo=self.ativo)

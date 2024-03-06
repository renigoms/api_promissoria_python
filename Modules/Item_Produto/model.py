class ItemProduto:
    def __init__(self, id: int, id_contrato: int, id_produto: int, valor_venda: float, ativo: bool):
        self.id = id
        self.id_contrato = id_contrato
        self.id_produto = id_produto
        self.valor_venda = valor_venda
        self.ativo = ativo

    def to_dict(self):
        return dict(id=self.id,
                    id_contrato=self.id_contrato,
                    id_produto=self.id_produto,
                    valor_venda=self.valor_venda,
                    ativo=self.ativo)

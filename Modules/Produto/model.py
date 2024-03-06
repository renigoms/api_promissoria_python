class Produto:
    def __init__(self, nome=None, unid_medida=None, valor_unit=None, porc_lucro=None, id=None, ativo=None):
        self.id = id
        self.nome = nome
        self.unid_medida = unid_medida
        self.valor_unit = valor_unit
        self.porc_lucro = porc_lucro
        self.ativo = ativo

    def to_dict(self):
        return dict(id=self.id,
                    nome=self.nome,
                    unid_medida=self.unid_medida,
                    valor_unit=self.valor_unit,
                    porc_lucro=self.porc_lucro,
                    ativo=self.ativo, )

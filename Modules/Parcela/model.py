class Parcela:
    def __init__(self, id=None, id_contrato=None, valor=None, data_pag=None, paga=None, ativo=None):
        self.id = id
        self.id_contrato = id_contrato
        self.valor = valor
        self.data_pag = data_pag.strftime('%d-%m-%Y') if data_pag is not None else None
        self.paga = paga
        self.ativo = ativo

    def to_dict(self):
        return dict(id=self.id,
                    id_contrato=self.id_contrato,
                    valor=self.valor,
                    data_pag=self.data_pag,
                    paga=self.paga,
                    ativo=self.ativo)

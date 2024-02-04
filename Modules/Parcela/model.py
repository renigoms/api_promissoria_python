class Parcela:
    def __init__(self, id=None, id_contrato=None, valor=None, data_pag=None, status=None):
        self._id = id
        self._id_contrato = id_contrato
        self._valor = valor
        self._data_pag = data_pag.strftime('%d-%m-%Y') if data_pag is not None else None
        self._status = status

    def __str__(self):
        return "Parcela: id={}, id_contrato={}, valor={}, data_pag={}, status={}".format(
            self._id, self._id_contrato, self._valor, self._data_pag, self._status) \
            if self._id is not None \
            else "Parcela: id_contrato={}, valor={}, data_pag={}, status={}".format(
            self._id_contrato, self._valor, self._data_pag, self._status)

    @property
    def id_contrato(self):
        return self._id_contrato

    @property
    def valor(self):
        return self._valor

    @property
    def data_pag(self):
        return self._data_pag

    @property
    def status(self):
        return self._status

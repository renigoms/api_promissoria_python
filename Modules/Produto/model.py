class Produto:
    def __init__(self, nome=None, unid_medida=None, valor_unit=None, porc_lucro=None, id=None):
        self._id = id
        self._nome = nome
        self._unid_medida = unid_medida
        self._valor_unit = valor_unit
        self._porc_lucro = porc_lucro

    def __str__(self):
        return ("Produto: id={}, nome={}, unid_medida={}, valor_unit={}, "
                "porc_lucro={}").format(self._id, self._nome, self._unid_medida,
                                        self._valor_unit, self._porc_lucro) \
            if self._id is not None \
            else ("Produto:  nome={}, unid_medida={}, valor_unit={}, "
                  "porc_lucro={}").format(self._nome, self._unid_medida,
                                          self._valor_unit, self._porc_lucro)

    @property
    def id(self): return self._id

    @property
    def nome(self): return self._nome

    @property
    def unid_medida(self): return self._unid_medida

    @property
    def valor_unit(self): return self._valor_unit

    @property
    def porc_lucro(self): return self._porc_lucro

from Util.SQLGeral import SQLGeral


class SQLContrato:
    NAME_TABLE = "Contrato"

    _ID_CLIENTE = "id_cliente"

    _ITENS_PRODUTO = "itens_produto"

    _VALOR_UNIT_BY_PRODUTO = "produto.valor_unit"

    _PORC_LUCRO_BY_PRODUTO = "produto.porc_lucro"

    _PAGA_BY_PACELA = "parcela.paga"

    _ID_CONTRATO_BY_PARCELA = "parcela.id_contrato"

    _NUM_PARCLS = "num_parcelas"

    _VALOR = "valor"

    _DESCRICAO = "descricao"

    _DATA_CRIACAO = "data_criacao"

    _PARCELAS_DEFINIDAS = "parcelas_definidas"

    @staticmethod
    def CREATE_TABLE():
        from Modules.Cliente.SQL import SQLCliente
        return f"""CREATE TABLE IF NOT EXISTS {SQLContrato.NAME_TABLE}(
                            {SQLGeral.ID_QUERY},
                            {SQLContrato._ID_CLIENTE} INT REFERENCES {SQLCliente.NAME_TABLE} ({SQLGeral.ID}) NOT NULL,
                            {SQLContrato._NUM_PARCLS} INT NOT NULL,
                            {SQLContrato._DATA_CRIACAO} DATE DEFAULT CURRENT_DATE,
                            {SQLContrato._VALOR} NUMERIC NOT NULL,
                            {SQLContrato._DESCRICAO} VARCHAR(200) NOT NULL,
                            {SQLContrato._PARCELAS_DEFINIDAS} BOOL DEFAULT FALSE,
                            {SQLGeral.ATIVO_QUERY}   
                    );"""

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)

    @staticmethod
    def _SELECT_ID_CLIENTE_BY_CPF():
        from Modules.Cliente.SQL import SQLCliente
        CLIENTE_CPF = "cpf"
        return f"""SELECT {SQLGeral.ID} FROM {SQLCliente.NAME_TABLE} 
                    WHERE {CLIENTE_CPF} ILIKE %s"""

    SELECT_BY_SEARCH = f"""{SELECT_ALL} WHERE ({SQLGeral.ID} = %s) 
                            OR ({_ID_CLIENTE} IN ({_SELECT_ID_CLIENTE_BY_CPF()}));"""

    @staticmethod
    def SELECT_VAL_PORC_LUCRO_PRODUTO():
        from Modules.Produto.SQL import SQLProduto
        return (f"SELECT {SQLContrato._VALOR_UNIT_BY_PRODUTO},"
                f"{SQLContrato._PORC_LUCRO_BY_PRODUTO} FROM {SQLProduto.NAME_TABLE} "
                f"WHERE {SQLGeral.ID} = %s;")

    @staticmethod
    def SELECT_STATUS_PACELAS():
        from Modules.Parcela.SQL import SQLParcela
        return (f"SELECT {SQLContrato._PAGA_BY_PACELA} "
                f"FROM {SQLContrato.NAME_TABLE} INNER JOIN {SQLParcela.NAME_TABLE} "
                f"ON {SQLContrato._ID_CONTRATO_BY_PARCELA} = %s;")

    CREATE = (f"INSERT INTO {NAME_TABLE} ({_ID_CLIENTE}, "
              f"{_NUM_PARCLS}, {_VALOR}, {_DESCRICAO}) "
              f"VALUES (%s,%s,%s,%s);")

    UPDATE_PARCELAS_DEFINIDAS = f"""UPDATE {NAME_TABLE} SET {_PARCELAS_DEFINIDAS} = TRUE WHERE {SQLGeral.ID}=%s;"""

    DEFINIR_PARCELAS = f"""UPDATE {NAME_TABLE} SET {_PARCELAS_DEFINIDAS} = TRUE WHERE {SQLGeral.ID}=%s;"""

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE, SQLGeral.ID)

    AUTO_ITENS = [SQLGeral.ID, _DATA_CRIACAO, _VALOR, SQLGeral.ATIVO, _PARCELAS_DEFINIDAS]

    REQUEST_ITENS = [_ID_CLIENTE, _NUM_PARCLS, _DESCRICAO, _ITENS_PRODUTO]
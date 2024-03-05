from Util.SQLGeral import SQLGeral



class SQLCliente:
    NAME_TABLE = "Cliente"
    _NOME_COMPLETO = "nome_completo"
    _CPF = "cpf"
    _EMAIL = "email"
    _TELEFONE = "telefone"
    _CONTRATO_ID_CLIENTE = 'id_cliente'
    CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {NAME_TABLE}(
                    {SQLGeral.ID_QUERY},
                    {_NOME_COMPLETO} VARCHAR(200) NOT NULL,
                    {_CPF} VARCHAR(14) UNIQUE NOT NULL,
                    {_EMAIL} VARCHAR(100) NOT NULL,
                    {_TELEFONE} VARCHAR(100) NOT NULL,
                    {SQLGeral.ATIVO_QUERY});"""

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)

    SELECT_BY_SEARCH = f"""{SELECT_ALL} WHERE ({SQLGeral.ID} = %s) 
                            OR ({_NOME_COMPLETO} ILIKE %s) OR ({_CPF} ILIKE %s);"""

    @staticmethod
    def SELECT_ID_CLIENTE_IN_CONTRATO():
        from Modules.Contrato.SQL import SQLContrato
        return f"""SELECT {SQLCliente._CONTRATO_ID_CLIENTE} FROM {SQLContrato.NAME_TABLE};"""

    @staticmethod
    def SELECT_ATIVO_CONTRATO_BY_ID_CLIENTE():
        from Modules.Contrato.SQL import SQLContrato
        return f"""SELECT {SQLGeral.ATIVO} FROM {SQLContrato.NAME_TABLE}
                        WHERE {SQLCliente._CONTRATO_ID_CLIENTE} = %s;"""

    SELECT_COLUNMS_CLIENTE = f"""SELECT {SQLGeral.ATIVO}, {_NOME_COMPLETO}, {SQLGeral.ID} 
                                         FROM {NAME_TABLE} WHERE {_CPF} ILIKE  %s;"""

    CREATE = (f"INSERT INTO {NAME_TABLE} ({_NOME_COMPLETO},"
              f"{_CPF}, {_EMAIL}, {_TELEFONE}) VALUES (%s,%s,%s,%s);")

    UPDATE = (f"UPDATE {NAME_TABLE} "
              f"SET {_NOME_COMPLETO} = %s, {_CPF} = %s,  "
              f"{_EMAIL} = %s, {_TELEFONE} = %s "
              f"WHERE {SQLGeral.ID} = %s")

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE, SQLGeral.ID)

    ACTIVE_CLIENT = SQLGeral.ATIVAR(NAME_TABLE, _CPF)

    REQUERED_ITENS = [_NOME_COMPLETO, _CPF, _EMAIL, _TELEFONE]

from Util.SQLGeral import SQLGeral


class SQLCliente:
    NAME_TABLE = "Cliente"
    _NOME_COMPLETO = "nome_completo"
    _CPF = "cpf"
    _EMAIL = "email"
    _TELEFONE = "telefone"
    CREATE_TABLE = (f"CREATE TABLE IF NOT EXISTS {NAME_TABLE} ({SQLGeral.ID_QUERY},"
                    f"{_NOME_COMPLETO} VARCHAR(200) NOT NULL,"
                    f"{_CPF} VARCHAR(14) UNIQUE NOT NULL,"
                    f"{_EMAIL} VARCHAR(100) NOT NULL,"
                    f"{_TELEFONE} VARCHAR(100) NOT NULL);")

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)

    SELECT_BY_ID = f"{SELECT_ALL} WHERE {SQLGeral.ID} = %s;"

    SELECT_BY_CPF = f"{SELECT_ALL} WHERE {_CPF} ILIKE %s;"

    CREATE = (f"INSERT INTO {NAME_TABLE} ({_NOME_COMPLETO},"
              f"{_CPF}, {_EMAIL}, {_TELEFONE}) VALUES (%s,%s,%s,%s);")

    UPDATE = (f"UPDATE {NAME_TABLE} "
              f"SET {_NOME_COMPLETO} = %s, {_CPF} = %s,  "
              f"{_EMAIL} = %s, {_TELEFONE} = %s "
              f"WHERE {SQLGeral.ID} = %s")

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE)

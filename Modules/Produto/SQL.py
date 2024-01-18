from Util.SQLGeral import SQLGeral


class SQLProduto:
    NAME_TABLE = "Produto"
    _NAME = "nome"
    _UNID_MEDIDA = "unid_medida"
    _VALOR_UNIT = "valor_unit"
    _PORCENT_LUCRO = "porc_lucro"
    CREATE_TABLE = (f"CREATE TABLE IF NOT EXISTS {NAME_TABLE}( "
                    f"{SQLGeral.ID_QUERY}, {_NAME} VARCHAR(200) UNIQUE NOT NULL, "
                    f"{_UNID_MEDIDA} VARCHAR(100) NOT NULL, {_VALOR_UNIT} NUMERIC NOT NULL, "
                    f"{_PORCENT_LUCRO} NUMERIC DEFAULT 0.30);")

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)
    SELECT_BY_ID = f"{SELECT_ALL} WHERE {SQLGeral.ID} = %s"
    SELECT_BY_NAME = f"{SELECT_ALL} WHERE {_NAME} ILIKE %s;"

    CREATE_WITH_PORC_LUCRO = (f"INSERT INTO {NAME_TABLE} "
                              f"({_NAME}, {_UNID_MEDIDA}, {_VALOR_UNIT}, {_PORCENT_LUCRO})"
                              f"VALUES (%s, %s, %s, %s);")

    CREATE_WITH_PORC_LUCRO_DEFAULT = (f"INSERT INTO {NAME_TABLE} "
                                      f"({_NAME}, {_UNID_MEDIDA}, {_VALOR_UNIT}) "
                                      f"VALUES (%s, %s, %s);")

    UPDATE = (f"UPDATE {NAME_TABLE} SET {_NAME} = %s,"
              f" {_UNID_MEDIDA} = %s ,{_VALOR_UNIT} = %s, "
              f"{_PORCENT_LUCRO} = %s WHERE {SQLGeral.ID} = %s;")

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE)

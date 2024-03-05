from Util.SQLGeral import SQLGeral


class SQLProduto:
    NAME_TABLE = "Produto"
    _NAME = "nome"
    _UNID_MEDIDA = "unid_medida"
    _VALOR_UNIT = "valor_unit"
    _PORCENT_LUCRO = "porc_lucro"
    CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {NAME_TABLE}(
                        {SQLGeral.ID_QUERY},
                        {_NAME} VARCHAR(200) UNIQUE NOT NULL, 
                        {_UNID_MEDIDA} VARCHAR(100) NOT NULL, 
                        {_VALOR_UNIT} NUMERIC NOT NULL, 
                        {_PORCENT_LUCRO} NUMERIC DEFAULT 0.30,
                        {SQLGeral.ATIVO_QUERY});"""

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)

    SELECT_BY_SEARCH = f"""{SELECT_ALL} WHERE ({SQLGeral.ID} = %s) OR ({_NAME} ILIKE %s);"""

    SELECT_COL_ATIVO_PRODUTO = f"""SELECT {SQLGeral.ATIVO}, {SQLGeral.ID} 
                                    FROM {NAME_TABLE} WHERE {_NAME} ILIKE %s;"""

    CREATE_WITH_PORC_LUCRO = f"""INSERT INTO {NAME_TABLE} (
                                {_NAME}, {_UNID_MEDIDA}, {_VALOR_UNIT}, {_PORCENT_LUCRO}
                                ) VALUES (%s, %s, %s, %s);"""

    CREATE_WITH_PORC_LUCRO_DEFAULT = f"""INSERT INTO {NAME_TABLE} (
                                        {_NAME}, {_UNID_MEDIDA}, {_VALOR_UNIT}
                                        ) VALUES (%s, %s, %s);"""

    UPDATE = f"""UPDATE {NAME_TABLE} SET {_NAME} = %s, 
               {_UNID_MEDIDA} = %s ,{_VALOR_UNIT} = %s, 
              {_PORCENT_LUCRO} = %s WHERE {SQLGeral.ID} = %s;"""

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE, SQLGeral.ID)

    ACTIVE_PRODUTO = SQLGeral.ATIVAR(NAME_TABLE, _NAME)

    REQUERED_ITENS = [_NAME, _UNID_MEDIDA, _VALOR_UNIT]

from Util.SQLGeral import SQLGeral


class SQLParcela:
    NAME_TABLE = "Parcela"
    _NAME_TABLE_CONTRATO = "Contrato"
    _STATUS = "status"
    _DATA_PAG = "data_pag"
    _VALOR = "valor"
    _ID_CONTRATO = "id_contrato"
    _VALOR_CONTRATO = 'valor'
    _DATA_CRIACAO_CONTRATO = 'data_criacao'
    _QNT_PARCELAS_CONTRATO = 'num_parcelas'
    _PARCELAS_DEFINIDAS = "parcelas_definidas"

    CREATE_TABLE = (f"CREATE TABLE IF NOT EXISTS {NAME_TABLE}({SQLGeral.ID_QUERY}, "
                    f"{_ID_CONTRATO} INT REFERENCES {_NAME_TABLE_CONTRATO} "
                    f"({SQLGeral.ID}) ON DELETE CASCADE NOT NULL, "
                    f"{_VALOR} NUMERIC NOT NULL, {_DATA_PAG} DATE NOT NULL,"
                    f"{_STATUS} VARCHAR(100) DEFAULT 'EM ABERTO'); ")

    SELECT_BY_ID_CONTRATO = f"SELECT * FROM {NAME_TABLE} WHERE {_ID_CONTRATO} = %s"

    SELECT_CONTRATO = (f"SELECT {_QNT_PARCELAS_CONTRATO}, "
                       f"{_DATA_CRIACAO_CONTRATO}, {_VALOR_CONTRATO},"
                       f" {_PARCELAS_DEFINIDAS} FROM {_NAME_TABLE_CONTRATO}"
                       f" WHERE {SQLGeral.ID} = %s;")

    SELECT_BY_DATA_PAG = f"{SQLGeral.SELECT_ALL(NAME_TABLE)} WHERE {_ID_CONTRATO} = %s AND {_DATA_PAG} = %s;"

    CREATE = (f"INSERT INTO {NAME_TABLE} ({_ID_CONTRATO}, {_VALOR}, {_DATA_PAG}) "
              f"VALUES (%s,%s,%s)")

    UPDATE = f"UPDATE {NAME_TABLE} SET {_STATUS} = %s WHERE {_ID_CONTRATO} = %s AND {_DATA_PAG} = %s;"

class SQLGeral:
    ID = 'id'

    ID_QUERY = f"{ID} SERIAL PRIMARY KEY"

    ATIVO = "ativo"

    ATIVO_QUERY = f"{ATIVO} BOOL DEFAULT TRUE"

    DELETE_SQL = lambda NAME_TABLE, COLUMN_FILTER: f"""UPDATE {NAME_TABLE} 
            SET {SQLGeral.ATIVO} = FALSE WHERE {COLUMN_FILTER} = %s;"""

    SELECT_ALL = lambda NAME_TABLE: f"SELECT * FROM {NAME_TABLE}"

    SELECT_COL_ATIVO = lambda NAME_TABLE, BUSC_BY: f"""SELECT {SQLGeral.ATIVO} FROM {NAME_TABLE} 
                                                        WHERE {BUSC_BY} ILIKE %s;"""

    ATIVAR = lambda NAME_TABLE, BUSC_BY: f"""UPDATE {NAME_TABLE} SET {SQLGeral.ATIVO} = TRUE 
                                                {BUSC_BY} ILIKE %s;"""

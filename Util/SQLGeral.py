class SQLGeral:
    ID = 'id'

    ID_QUERY = f"{ID} SERIAL PRIMARY KEY"

    DELETE_SQL = lambda NAME_TABLE: f"DELETE FROM {NAME_TABLE} WHERE {SQLGeral.ID} = %s;"

    SELECT_ALL = lambda NAME_TABLE: f"SELECT * FROM {NAME_TABLE}"

from Modules.Cliente.SQL import SQLCliente
from Modules.Parcela.SQL import SQLParcela
from Modules.Produto.SQL import SQLProduto
from Util.SQLGeral import SQLGeral


class SQLContrato:
    NAME_TABLE = "Contrato"

    _ID_CLIENTE = "id_cliente"

    _ID_PRODUTO = "id_produto"

    _VALOR_UNIT_BY_PRODUTO = "produto.valor_unit"

    _PORC_LUCRO_BY_PRODUTO = "produto.porc_lucro"

    _STATUS_BY_PACELA = "parcela.status"

    _ID_CONTRATO_BY_PARCELA = "parcela.id_contrato"

    _NUM_PARCLS = "num_parcelas"

    _VALOR = "valor"

    _QNT_PRODUTO = "qnt_produto"

    _DESCRICAO = "descricao"

    _DATA_CRIACAO = "data_criacao"

    _PARCELAS_DEFINIDAS = "parcelas_definidas"

    _CLIENTE_CPF = "cpf"

    CREATE_TABLE = (f"CREATE TABLE IF NOT EXISTS {NAME_TABLE}({SQLGeral.ID_QUERY},"
                    f"{_ID_CLIENTE} INT REFERENCES {SQLCliente.NAME_TABLE} ({SQLGeral.ID}) "
                    f"NOT NULL,{_ID_PRODUTO} INT REFERENCES {SQLProduto.NAME_TABLE} ({SQLGeral.ID}) NOT NULL, "
                    f"{_NUM_PARCLS} INT NOT NULL, {_DATA_CRIACAO} DATE DEFAULT CURRENT_DATE, "
                    f"{_QNT_PRODUTO} INT NOT NULL, {_VALOR} NUMERIC NOT NULL, "
                    f"{_DESCRICAO} VARCHAR(200) NOT NULL, {_PARCELAS_DEFINIDAS} BOOL DEFAULT FALSE);")

    SELECT_ALL = SQLGeral.SELECT_ALL(NAME_TABLE)

    SELECT_BY_ID = f"{SELECT_ALL} WHERE {SQLGeral.ID} = %s;"

    SELECT_VAL_PORC_LUCRO_PRODUTO = (f"SELECT {_VALOR_UNIT_BY_PRODUTO},"
                                     f"{_PORC_LUCRO_BY_PRODUTO} FROM {SQLProduto.NAME_TABLE} "
                                     f"WHERE {SQLGeral.ID} = %s;")

    SELECT_STATUS_PACELAS = (f"SELECT {_STATUS_BY_PACELA} "
                             f"FROM {NAME_TABLE} INNER JOIN {SQLParcela.NAME_TABLE} "
                             f"ON {_ID_CONTRATO_BY_PARCELA} = %s;")

    _SELECT_ID_CLIENTE_BY_CPF = (f"SELECT {SQLGeral.ID} FROM {SQLCliente.NAME_TABLE}"
                                 f" WHERE {_CLIENTE_CPF} ILIKE %s")

    SELECT_BY_CPF_CLIENTE = (f"{SQLGeral.SELECT_ALL(NAME_TABLE)}"
                             f" WHERE {_ID_CLIENTE} IN ({_SELECT_ID_CLIENTE_BY_CPF});")

    CREATE = (f"INSERT INTO {NAME_TABLE} ({_ID_CLIENTE}, {_ID_PRODUTO}, "
              f"{_NUM_PARCLS}, {_QNT_PRODUTO}, {_VALOR}, {_DESCRICAO}) "
              f"VALUES (%s,%s,%s,%s,%s, %s)")

    DELETE = SQLGeral.DELETE_SQL(NAME_TABLE)

from Modules.Contrato.SQL import SQLContrato
from Modules.Produto.SQL import SQLProduto
from Util.SQLGeral import SQLGeral


class SQLItemProduto:
    NAME_TABLE = "item_produto"

    _ID_CONTRATO = "id_contrato"

    _ID_PRODUTO = "id_produto"

    _VALOR_VENDA = "valor_venda"

    CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {NAME_TABLE}(
                        {SQLGeral.ID_QUERY},
                        {_ID_CONTRATO} INT REFERENCES {SQLContrato.NAME_TABLE} ({SQLGeral.ID}) NOT NULL,
                        {_ID_PRODUTO} INT REFERENCES {SQLProduto.NAME_TABLE} ({SQLGeral.ID}) NOT NULL,
                        {_VALOR_VENDA} NUMERIC NOT NULL,
                        {SQLGeral.ATIVO_QUERY});"""

    CREATE = f"""INSERT INTO {NAME_TABLE} ({_ID_CONTRATO}, {_ID_PRODUTO}, {_VALOR_VENDA})
                VALUES (%s, %s, %s);"""

    SELECT_BY_ID_CONTRATO = f"{SQLGeral.SELECT_ALL(NAME_TABLE)} WHERE {_ID_CONTRATO} = %s;"

    SELECT_ID_PRODUTO_IN_ITEM_PRODUTO = f"SELECT {_ID_PRODUTO} FROM {NAME_TABLE};"

    SELECT_ATIVO_ITEM_PRODUTO_BY_ID_PRODUTO = f"""SELECT {SQLGeral.ATIVO} FROM {NAME_TABLE} 
                                                    WHERE {_ID_PRODUTO} = %s;"""

    DESATIVAR_ITEM_PRODUTO = SQLGeral.DELETE_SQL(NAME_TABLE, _ID_CONTRATO)


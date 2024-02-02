import psycopg2

from Modules.Cliente.model import Cliente
from Modules.Contrato.model import Contrato
from Modules.Parcela.model import Parcela
from Modules.Produto.model import Produto
from Services.Exceptions import IDException


class UtilGeral:
    @staticmethod
    def _get_select_dict(query: str, *args) -> dict:
        from Services.Connect_db_pg import Connection_db, Cursor
        with (Connection_db(**Cursor().dicio2) as cursor):
            cursor.execute(query, tuple(args))
            result_cursor = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            return [dict(zip(cols, i)) for i in result_cursor]

    getSelectDictCliente = lambda query, *args: [Cliente(**i) for i in UtilGeral._get_select_dict(query, *args)]

    getSelectDictProduto = lambda query, *args: [Produto(**i) for i in UtilGeral._get_select_dict(query, *args)]

    getSelectDictContrato = lambda query, *args: [Contrato(**i) for i in UtilGeral._get_select_dict(query, *args)]

    getSelectDictParcela = lambda query, *args: [Parcela(**i) for i in UtilGeral._get_select_dict(query, *args)]

    get_Val_Update = lambda oldValue, newValue: oldValue if newValue is None else newValue

    @staticmethod
    def execute_delete(sql_delete: str, index: str):
        try:
            from Services.Connect_db_pg import Cursor
            if index == "":
                raise IDException()
            return Cursor().execute(sql_delete, index)
        except IDException as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def is_product_exists(id_product: str) -> bool:
        from Modules.Produto.DAO import DAOProduto
        getProduct = DAOProduto.get_by_id(id_product)
        return len(getProduct) == 0

    @staticmethod
    def is_client_exists(id_client: str) -> bool:
        from Modules.Cliente.DAO import DAOCliente
        getClient = DAOCliente.get_by_id(id_client)
        return len(getClient) == 0

    @staticmethod
    def is_contract_exists(id_contract: str) -> bool:
        from Modules.Contrato.DAO import DAOContrato
        getContract = DAOContrato.get_by_id(id_contract)
        return len(getContract) == 0

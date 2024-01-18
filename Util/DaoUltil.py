import psycopg2

from Modules.Cliente.model import Cliente
from Modules.Contrato.model import Contrato
from Modules.Parcela.model import Parcela
from Modules.Produto.model import Produto
from Services.Exceptions import IDException


class UtilGeral:
    @staticmethod
    def getSelectDictCliente(query: str, *args):
        from Services.Connect_db_pg import Connection_db, Cursor
        with (Connection_db(**Cursor().dicio2) as cursor):
            cursor.execute(query, tuple(args))
            result_cursor = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            result = [dict(zip(cols, i)) for i in result_cursor]
            return [Cliente(**i) for i in result]

    @staticmethod
    def getSelectDictProduto(query: str, *args):
        from Services.Connect_db_pg import Connection_db, Cursor
        with Connection_db(**Cursor().dicio2) as cursor:
            cursor.execute(query, tuple(args))
            result_cursor = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            result = [dict(zip(cols, i)) for i in result_cursor]
            return [Produto(**i) for i in result]

    @staticmethod
    def getSelectDictContrato(query: str, *args):
        from Services.Connect_db_pg import Connection_db, Cursor
        with Connection_db(**Cursor().dicio2) as cursor:
            cursor.execute(query, tuple(args))
            result_cursor = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            result = [dict(zip(cols, i)) for i in result_cursor]
            return [Contrato(**i) for i in result]

    @staticmethod
    def getSelectDictParcela(query: str, *args):
        from Services.Connect_db_pg import Connection_db, Cursor
        with Connection_db(**Cursor().dicio2) as cursor:
            cursor.execute(query, tuple(args))
            result_cursor = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            result = [dict(zip(cols, i)) for i in result_cursor]
            return [Parcela(**i) for i in result]

    get_Val_Update = lambda oldValue, newValue: (
        oldValue) if newValue is None else newValue

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

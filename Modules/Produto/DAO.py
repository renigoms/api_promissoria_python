import sys

import psycopg2

from Modules.Produto.SQL import SQLProduto
from Modules.Produto.model import Produto

from Services.Exceptions import NullException, IDException, NotAlterException
from Util.DaoUltil import UtilGeral


class DAOProduto:

    create_table = SQLProduto.CREATE_TABLE

    get_all = UtilGeral.getSelectDictProduto(SQLProduto.SELECT_ALL)

    get_by_id = lambda id: UtilGeral.getSelectDictProduto(SQLProduto.SELECT_BY_ID, id)

    get_by_name = lambda name: UtilGeral.getSelectDictProduto(SQLProduto.SELECT_BY_NAME, name)

    @staticmethod
    def post_create(produto: Produto):
        try:
            from Services.Connect_db_pg import Cursor
            if (produto.nome is None
                    or produto.unid_medida is None
                    or produto.valor_unit is None):
                raise NullException()
            return Cursor().execute(SQLProduto.CREATE_WITH_PORC_LUCRO_DEFAULT,
                                    produto.nome,
                                    produto.unid_medida,
                                    produto.valor_unit) \
                if produto.porc_lucro is None \
                else Cursor().execute(SQLProduto.CREATE_WITH_PORC_LUCRO,
                                      produto.nome,
                                      produto.unid_medida,
                                      produto.valor_unit,
                                      produto.porc_lucro)

        except NullException as e:
            raise e
        except psycopg2.errors.UniqueViolation as e:
            raise e
        except Exception as e:
            print(f"Erro {e.__str__()} ao salvar, tente novamente !!!")
            print(f"-> {sys.exc_info()}")
            return False

    @staticmethod
    def put_update(produto: Produto, id: str):
        try:
            from Services.Connect_db_pg import Cursor
            if id is None or id == "":
                raise IDException()

            if produto.id is not None:
                raise NotAlterException()

            oldProduto = DAOProduto.get_by_id(id)

            nome = UtilGeral.get_Val_Update(oldProduto[0].nome, produto.nome)
            unid_medida = UtilGeral.get_Val_Update(oldProduto[0].unid_medida, produto.unid_medida)
            valor_unit = UtilGeral.get_Val_Update(oldProduto[0].valor_unit, produto.valor_unit)
            porc_lucro = UtilGeral.get_Val_Update(oldProduto[0].porc_lucro, produto.porc_lucro)

            return Cursor().execute(SQLProduto.UPDATE, nome, unid_medida, valor_unit, porc_lucro, id)
        except IDException as e:
            raise e
        except NotAlterException as e:
            raise e
        except Exception as e:
            print(e)
            print(sys.exc_info())

    @staticmethod
    def delete(id: str):
        try:
            return UtilGeral.execute_delete(SQLProduto.DELETE, id)
        except IDException as e:
            raise e
        except psycopg2.errors.ForeignKeyViolation as e:
            raise e
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            print(sys.exc_info())

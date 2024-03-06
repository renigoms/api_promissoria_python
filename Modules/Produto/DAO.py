import sys

import psycopg2

from Modules.Item_Produto.SQL import SQLItemProduto
from Modules.Produto.SQL import SQLProduto
from Modules.Produto.model import Produto
from Services.Exceptions import NullException, IDException, NotAlterException, ProductException, ForeingKeyException, \
    ReactiveException
from Util.DaoUltil import UtilGeral
from Util.SQLGeral import SQLGeral


class DAOProduto:
    create_table = SQLProduto.CREATE_TABLE

    get_all = UtilGeral.getSelectDictProduto(SQLProduto.SELECT_ALL)
    
    @staticmethod
    def get_by_search(search:str):
        search_id = 0
        try:
            search_id = int(search)
        except ValueError:
            pass
        return UtilGeral.getSelectDictProduto(SQLProduto.SELECT_BY_SEARCH,
                            search_id, UtilGeral.ADD_SIDES("%", search))

    REQUERED_ITEMS = SQLProduto.REQUERED_ITENS

    @staticmethod
    def post_create(produto: Produto):
        global Cursor
        try:
            from Services.Connect_db_pg import Cursor
            if produto.id is not None:
                raise IDException()
            if UtilGeral.is_requered_itens_null(produto.__dict__, DAOProduto.REQUERED_ITEMS):
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
        except IDException as e:
            raise e
        except psycopg2.errors.UniqueViolation as e:
            list_col_ativo = Cursor().query(SQLProduto.SELECT_COL_ATIVO_PRODUTO, produto.nome)
            if list_col_ativo[0]['ativo'] is not True:
                if Cursor().execute(SQLProduto.ACTIVE_PRODUTO, produto.nome):
                    DAOProduto.put_update(produto, list_col_ativo[0][SQLGeral.ID])
                    raise ReactiveException()
            raise e
        except ReactiveException as e:
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

            if UtilGeral.is_not_product_exists(id):
                raise ProductException()

            oldProduto = DAOProduto.get_by_search(id)

            nome = UtilGeral.get_Val_Update(oldProduto[0].nome, produto.nome)
            unid_medida = UtilGeral.get_Val_Update(oldProduto[0].unid_medida, produto.unid_medida)
            valor_unit = UtilGeral.get_Val_Update(oldProduto[0].valor_unit, produto.valor_unit)
            porc_lucro = UtilGeral.get_Val_Update(oldProduto[0].porc_lucro, produto.porc_lucro)

            return Cursor().execute(SQLProduto.UPDATE, nome, unid_medida, valor_unit, porc_lucro, id)
        except IDException as e:
            raise e
        except NotAlterException as e:
            raise e
        except ProductException as e:
            raise e
        except Exception as e:
            print(e)
            print(sys.exc_info())

    @staticmethod
    def delete(id: str):
        try:
            if UtilGeral.is_not_product_exists(id):
                raise ProductException()

            produto_com_contrato = Cursor().query(SQLItemProduto.SELECT_ID_PRODUTO_IN_ITEM_PRODUTO)

            for id_produto_list in produto_com_contrato:
                if id_produto_list['id_produto'] == int(id):
                    is_contrato_ativo = Cursor().query(SQLItemProduto.SELECT_ATIVO_ITEM_PRODUTO_BY_ID_PRODUTO, id)
                    for ativo_list in is_contrato_ativo:
                        if ativo_list['ativo']:
                            raise ForeingKeyException()
            return UtilGeral.execute_delete(SQLProduto.DELETE, id)
        except IDException as e:
            raise e
        except psycopg2.errors.UniqueViolation as e:
            raise e
        except ForeingKeyException as e:
            raise e
        except ProductException as e:
            raise e
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            print(sys.exc_info())

import sys

import psycopg2

from Modules.Cliente.SQL import SQLCliente
from Modules.Cliente.model import Cliente
from Services.Connect_db_pg import Cursor
from Services.Exceptions import NullException, IDException, NotAlterException, ClientException, ForeingKeyException, \
    ReactiveException
from Util.DaoUltil import UtilGeral
from Util.SQLGeral import SQLGeral


class DAOCliente:
    create_table = SQLCliente.CREATE_TABLE

    get_all = UtilGeral.getSelectDictCliente(SQLCliente.SELECT_ALL)

    @staticmethod
    def get_by_search(search: str):
        search_id = 0
        try:
            search_id = int(search)
        except ValueError as e:
            pass

        return UtilGeral.getSelectDictCliente(SQLCliente.SELECT_BY_SEARCH, search_id,
                                              UtilGeral.ADD_SIDES("%", search),
                                              UtilGeral.ADD_SIDES("%", search, False),
                                              search_id)

    REQUERED_ITEMS = SQLCliente.REQUERED_ITENS

    @staticmethod
    def post_create(cliente: Cliente):
        try:
            if cliente.id is not None:
                raise IDException()
            if UtilGeral.is_requered_itens_null(cliente.__dict__, DAOCliente.REQUERED_ITEMS):
                raise NullException()
            return Cursor().execute(SQLCliente.CREATE,
                                    cliente.nome_completo,
                                    cliente.cpf,
                                    cliente.email,
                                    cliente.telefone)

        except NullException as e:
            raise e
        except IDException as e:
            raise e
        except psycopg2.errors.UniqueViolation as e:
            list_col_ativo = Cursor().query(SQLCliente.SELECT_COLUNMS_CLIENTE, cliente.cpf)
            if (list_col_ativo[0]['ativo'] is not True
                    and list_col_ativo[0]['nome_completo'] == cliente.nome_completo):
                if Cursor().execute(SQLCliente.ACTIVE_CLIENT, cliente.cpf):
                    DAOCliente.put_update(cliente, list_col_ativo[0][SQLGeral.ID])
                    raise ReactiveException()
            raise e
        except ReactiveException as e:
            raise e
        except psycopg2.errors.StringDataRightTruncation as e:
            raise e
        except Exception as e:
            print(f"Erro {e.__str__()} ao salvar, tente novamente !!!")
            print(f"-> {sys.exc_info()}")
            return False

    @staticmethod
    def put_update(cliente: Cliente, id: str):
        try:
            if id is None or id == "":
                raise IDException()

            if UtilGeral.is_not_client_exists(id):
                raise ClientException()

            if cliente.id is not None:
                raise NotAlterException()

            oldCliente = DAOCliente.get_by_search(id)

            nome_completo = UtilGeral.get_Val_Update(oldCliente[0].nome_completo, cliente.nome_completo)
            cpf = UtilGeral.get_Val_Update(oldCliente[0].cpf, cliente.cpf)
            email = UtilGeral.get_Val_Update(oldCliente[0].email, cliente.email)
            telefone = UtilGeral.get_Val_Update(oldCliente[0].telefone, cliente.telefone)

            return Cursor().execute(SQLCliente.UPDATE, nome_completo, cpf, email, telefone, id)
        except IDException as e:
            raise e
        except NotAlterException as e:
            raise e
        except ClientException as e:
            raise e
        except Exception as e:
            print(e)
            print(sys.exc_info())

    @staticmethod
    def delete(id: str):
        try:
            if UtilGeral.is_not_client_exists(id):
                raise ClientException()

            cliente_com_contrato = Cursor().query(SQLCliente.SELECT_ID_CLIENTE_IN_CONTRATO())

            for id_cliente_list in cliente_com_contrato:
                if id_cliente_list['id_cliente'] == int(id):

                    is_contrato_ativo = Cursor().query(SQLCliente.SELECT_ATIVO_CONTRATO_BY_ID_CLIENTE(), id)

                    for ativo_list in is_contrato_ativo:
                        if ativo_list[SQLGeral.ATIVO]:
                            raise ForeingKeyException()

            return UtilGeral.execute_delete(SQLCliente.DELETE, id)
        except IDException as e:
            raise e
        except ForeingKeyException as e:
            raise e
        except ClientException as e:
            raise e
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            print(sys.exc_info())

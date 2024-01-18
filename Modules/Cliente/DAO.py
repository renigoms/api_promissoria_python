import sys

import psycopg2

from Modules.Cliente.SQL import SQLCliente
from Modules.Cliente.model import Cliente
from Services.Connect_db_pg import Cursor
from Services.Exceptions import NullException, IDException, NotAlterException
from Util.DaoUltil import UtilGeral


class DAOCliente:

    create_table = SQLCliente.CREATE_TABLE

    get_all = UtilGeral.getSelectDictCliente(SQLCliente.SELECT_ALL)

    get_by_id = lambda id: UtilGeral.getSelectDictCliente(SQLCliente.SELECT_BY_ID, id)

    get_by_cpf = lambda cpf: UtilGeral.getSelectDictCliente(SQLCliente.SELECT_BY_CPF, cpf)

    @staticmethod
    def post_create(cliente: Cliente):
        try:
            if (cliente.nome_completo is None
                    or cliente.cpf is None
                    or cliente.email is None
                    or cliente.telefone is None):
                raise NullException()
            return Cursor().execute(SQLCliente.CREATE,
                                    cliente.nome_completo,
                                    cliente.cpf,
                                    cliente.email,
                                    cliente.telefone)

        except NullException as e:
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

            if cliente.id is not None:
                raise NotAlterException()

            oldCliente = DAOCliente.get_by_id(id)

            nome_completo = UtilGeral.get_Val_Update(oldCliente[0].nome_completo, cliente.nome_completo)
            cpf = UtilGeral.get_Val_Update(oldCliente[0].cpf, cliente.cpf)
            email = UtilGeral.get_Val_Update(oldCliente[0].email, cliente.email)
            telefone = UtilGeral.get_Val_Update(oldCliente[0].telefone, cliente.telefone)

            return Cursor().execute(SQLCliente.UPDATE, nome_completo, cpf, email, telefone, id)
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
            return UtilGeral.execute_delete(SQLCliente.DELETE, id)
        except IDException as e:
            raise e
        except psycopg2.errors.ForeignKeyViolation as e:
            raise e
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            print(sys.exc_info())

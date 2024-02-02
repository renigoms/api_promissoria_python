import sys

from Modules.Contrato.SQL import SQLContrato
from Modules.Contrato.model import Contrato
from Services.Connect_db_pg import Cursor
from Services.Exceptions import AutoValueException, NullException, ParcelaEmAbertoExcerption, IDException, \
    ContractException, ClientException, ProductException
from Util.DaoUltil import UtilGeral


class DAOContrato:
    create_table = SQLContrato.CREATE_TABLE

    get_all = UtilGeral.getSelectDictContrato(SQLContrato.SELECT_ALL)

    get_by_id = lambda id: UtilGeral.getSelectDictContrato(SQLContrato.SELECT_BY_ID, id)

    get_by_cliente_cpf = lambda cpf: UtilGeral.getSelectDictContrato(SQLContrato.SELECT_BY_CPF_CLIENTE, cpf)

    _is_auto_elements = lambda contrato: (contrato.id is not None
                                          or contrato.data_criacao is not None
                                          or contrato.valor is not None
                                          or contrato.parcelas_definidas is True)

    _is_requered_elements = lambda contrato: (contrato.id_cliente is None
                                              or contrato.id_produto is None
                                              or contrato.num_parcelas is None
                                              or contrato.descricao is None)

    @staticmethod
    def post_create(contrato: Contrato):
        try:
            if DAOContrato._is_auto_elements(contrato):
                raise AutoValueException()
            if DAOContrato._is_requered_elements(contrato):
                raise NullException()
            if UtilGeral.is_client_exists(contrato.id_cliente):
                raise ClientException()
            if UtilGeral.is_product_exists(contrato.id_produto):
                raise ProductException()
            valor_unit_and_porc_lucro = UtilGeral.getSelectDictProduto(SQLContrato.SELECT_VAL_PORC_LUCRO_PRODUTO,
                                                                       contrato.id_produto)[0]
            valor = lambda x, y, z: (x * y + x) * z

            return Cursor().execute(SQLContrato.CREATE, contrato.id_cliente,
                                    contrato.id_produto, contrato.num_parcelas,
                                    contrato.qnt_produto,
                                    valor(
                                        valor_unit_and_porc_lucro.valor_unit,
                                        valor_unit_and_porc_lucro.porc_lucro,
                                        contrato.qnt_produto
                                    ),
                                    contrato.descricao)
        except NullException as e:
            raise e
        except AutoValueException as e:
            raise e
        except ClientException as e:
            raise e
        except ProductException as e:
            raise e
        except Exception as e:
            print(f"Erro {e} ao salvar !!!")
            print(sys.exc_info())
            return False

    @staticmethod
    def _is_full_parcelas_pagas(id: str):
        lista_status_parcela = UtilGeral.getSelectDictParcela(SQLContrato.SELECT_STATUS_PACELAS, id)
        for i in lista_status_parcela:
            if i.status == "EM ABERTO":
                return False
        return True

    @staticmethod
    def delete(id: str):
        try:
            if UtilGeral.is_contract_exists(id):
                raise ContractException()
            if DAOContrato._is_full_parcelas_pagas(id):
                return UtilGeral.execute_delete(SQLContrato.DELETE, id)
            raise ParcelaEmAbertoExcerption()
        except ParcelaEmAbertoExcerption as e:
            raise e
        except IDException() as e:
            raise e
        except ContractException as e:
            raise e
        except Exception as e:
            print(f"Erro ao deleta: {e}")
            print(sys.exc_info())
            return False

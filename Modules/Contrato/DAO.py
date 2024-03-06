import sys

from Modules.Cliente.DAO import DAOCliente
from Modules.Contrato.SQL import SQLContrato
from Modules.Contrato.model import Contrato
from Modules.Item_Produto.DAO import DAOItemProduto
from Modules.Item_Produto.SQL import SQLItemProduto
from Modules.Parcela.DAO import DAOParcela
from Modules.Parcela.SQL import SQLParcela
from Services.Connect_db_pg import Cursor
from Services.Exceptions import ParcelaEmAbertoExcerption, IDException, \
    ContractException, ClientException, ProductException
from Util.DaoUltil import UtilGeral


class DAOContrato:
    create_table = SQLContrato.CREATE_TABLE()

    get_all = UtilGeral.getSelectDictContrato(SQLContrato.SELECT_ALL)

    @staticmethod
    def get_by_search(search: str):
        search_id = 0
        try:
            search_id = int(search)
        except ValueError:
            pass

        return UtilGeral.getSelectDictContrato(SQLContrato.SELECT_BY_SEARCH, search_id, search)

    requered_items = SQLContrato.REQUEST_ITENS

    auto_items = SQLContrato.AUTO_ITENS

    @staticmethod
    def _calc_valor_total_contrato(ids_produto: list, somatorio: float = 0, count: int = 0) -> float:
        try:
            somatorio += UtilGeral.get_valor_venda_produto(ids_produto[count])
            count += 1
        except IndexError as e:
            return somatorio

        return DAOContrato._calc_valor_total_contrato(ids_produto, somatorio, count)

    @staticmethod
    def post_create(contrato: Contrato):
        try:
            if UtilGeral.is_not_client_exists(contrato.id_cliente):
                raise ClientException()

            for id_product in contrato.itens_produto:
                if UtilGeral.is_not_product_exists(id_product):
                    raise ProductException()

            valor_contrato = DAOContrato._calc_valor_total_contrato(contrato.itens_produto)

            create_contrato = Cursor().execute(SQLContrato.CREATE,
                                               contrato.id_cliente, contrato.num_parcelas,
                                               valor_contrato, contrato.descricao)

            if create_contrato:
                cliente = DAOCliente().get_by_search(contrato.id_cliente)

                listar_contratos = DAOContrato().get_by_search(cliente[0].cpf)

                contract_created = None

                for item_contrato in listar_contratos:
                    if not item_contrato.parcelas_definidas:
                        contract_created = item_contrato
                        break

                cont_sucess_items_product = DAOItemProduto().create_item_produto(
                    contrato.id_cliente, contrato.itens_produto, contract_created
                )

                cont_sucess_parcels = DAOParcela().create_parcela(
                    valor_contrato, contrato.num_parcelas, contract_created.id
                )

                if (cont_sucess_parcels == contrato.num_parcelas and
                        cont_sucess_items_product == len(contrato.itens_produto)):
                    return Cursor().execute(SQLContrato.DEFINIR_PARCELAS, contract_created.id)
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
        lista_status_parcela = UtilGeral.getSelectDictParcela(SQLContrato.SELECT_STATUS_PACELAS(), id)
        for i in lista_status_parcela:
            if not i.paga:
                return False
        return True

    @staticmethod
    def delete(id: str):
        try:
            if UtilGeral.is_not_contract_exists(id):
                raise ContractException()
            if DAOContrato._is_full_parcelas_pagas(id):
                if Cursor().execute(SQLParcela.DESATIVAR_PARCELAS, id) \
                        and Cursor().execute(SQLItemProduto.DESATIVAR_ITEM_PRODUTO, id):
                    return UtilGeral.execute_delete(SQLContrato.DELETE, id)
            raise ParcelaEmAbertoExcerption()
        except ParcelaEmAbertoExcerption as e:
            raise e
        except IDException as e:
            raise e
        except ContractException as e:
            raise e
        except Exception as e:
            print(f"Erro ao deleta: {e}")
            print(sys.exc_info())
            return False

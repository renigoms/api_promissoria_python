import psycopg2

from Modules.Cliente.model import Cliente
from Modules.Contrato.SQL import SQLContrato
from Modules.Contrato.model import Contrato
from Modules.Item_Produto.model import ItemProduto
from Modules.Parcela.model import Parcela
from Modules.Produto.model import Produto
from Services.Connect_db_pg import Cursor
from Services.Exceptions import IDException
from Util.SQLGeral import SQLGeral


class UtilGeral:
    
    @staticmethod
    def _get_Only_active_elements(query, *args):
        try:
            return [i for i in Cursor().query(query, *args) if i[SQLGeral.ATIVO]]
        except KeyError as e:
            return [i for i in Cursor().query(query, *args)]
    
    getSelectDictCliente = lambda query, *args: [Cliente(**i) for i in UtilGeral._get_Only_active_elements(query, *args)]

    getSelectDictProduto = lambda query, *args: [Produto(**i) for i in UtilGeral._get_Only_active_elements(query, *args)]

    getSelectDictContrato = lambda query, *args: [Contrato(**i) for i in UtilGeral._get_Only_active_elements(query, *args)]

    getSelectDictParcela = lambda query, *args: [Parcela(**i) for i in UtilGeral._get_Only_active_elements(query, *args)]

    getSelectDictItemProduto = lambda query, *args: [ItemProduto(**i) for i in UtilGeral._get_Only_active_elements(query, *args)]

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
    def is_not_product_exists(id_product: str) -> bool:
        from Modules.Produto.DAO import DAOProduto
        getProduct = DAOProduto.get_by_search(id_product)
        return len(getProduct) == 0

    @staticmethod
    def is_not_client_exists(id_client: str) -> bool:
        from Modules.Cliente.DAO import DAOCliente
        getClient = DAOCliente.get_by_search(id_client)
        return len(getClient) == 0

    @staticmethod
    def is_not_contract_exists(id_contract: str) -> bool:
        from Modules.Contrato.DAO import DAOContrato
        getContract = DAOContrato.get_by_search(id_contract)
        return len(getContract) == 0

    @staticmethod
    def is_not_parcels_exists(id_contrato: str, data_pag: str):
        from Modules.Parcela.DAO import DAOParcela
        get_parcela = DAOParcela.get_data_pag(id_contrato, data_pag)
        return len(get_parcela) == 0

    @staticmethod
    def is_auto_itens_not_null(dictMap: dict, list_auto_elements: list) -> bool:
        for camp in list_auto_elements:
            try:
                if dictMap[camp] is not None:
                    return True
            except KeyError as e:
                continue
        return False

    @staticmethod
    def is_requered_itens_null(dict_map: dict, list_requered_elements: list) -> bool:
        itens = [None, '', "", """""", 0, 0.0]
        for camp in list_requered_elements:
            try:
                if itens.__contains__(dict_map[camp]):
                    return True
            except KeyError as e:
                return True
        return False

    ADD_SIDES = lambda add_itens, texto_base, ambos_lados=True: \
        add_itens + (texto_base_str := str(texto_base) if isinstance(texto_base, int) else texto_base) + add_itens \
            if ambos_lados else (texto_base_str := str(texto_base) if isinstance(texto_base, int) else texto_base) + add_itens

    @staticmethod
    def get_valor_venda_produto(id_produto: int):
        if id_produto is not None:
            list_prod = UtilGeral.getSelectDictProduto(SQLContrato.SELECT_VAL_PORC_LUCRO_PRODUTO(), id_produto)

            valor_venda = list_prod[0].valor_unit * list_prod[0].porc_lucro + list_prod[0].valor_unit

            return valor_venda
        return 0

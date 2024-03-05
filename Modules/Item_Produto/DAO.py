from Modules.Contrato.model import Contrato
from Modules.Item_Produto.SQL import SQLItemProduto
from Services.Connect_db_pg import Cursor
from Util.DaoUltil import UtilGeral


class DAOItemProduto:
    GET_CREATE_TABLE = SQLItemProduto.CREATE_TABLE

    get_by_id = lambda id_contrato: UtilGeral.getSelectDictItemProduto(SQLItemProduto.SELECT_BY_ID_CONTRATO,
                                                                       id_contrato)

    @staticmethod
    def create_item_produto(id_cliente: int, itens_produto: list, contrato_list: list[Contrato]):
        cont_sucess_items_product = 0

        for id_produto in itens_produto:
            valor_venda = UtilGeral.get_valor_venda_produto(id_produto)
            if Cursor().execute(SQLItemProduto.CREATE, contrato_list[0].id,
                                id_produto, valor_venda):
                cont_sucess_items_product += 1
        return cont_sucess_items_product

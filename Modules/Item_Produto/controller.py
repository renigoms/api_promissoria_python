from flask import Blueprint

from Modules.Item_Produto.DAO import DAOItemProduto
from Util.ServerUtils import ResponseUtils


class ItemProdutoController:
    item_produto_controller = Blueprint('item_produto_controller', __name__)
    modulo_name = 'Item Produto'

    @staticmethod
    @item_produto_controller.route(f'/{modulo_name}/<id_contrato>', methods = ['GET'])
    def get_item(id_contrato):
        return ResponseUtils.get_response_busca(DAOItemProduto.get_by_id(id_contrato))
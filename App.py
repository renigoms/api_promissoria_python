from flask import Flask


from Modules.Cliente.Controller import ClienteController
from Modules.Contrato.controller import ContratoController
from Modules.Item_Produto.controller import ItemProdutoController
from Modules.Parcela.controller import ParcelaController
from Modules.Produto.controller import ProdutoController
from Services.Connect_db_pg import Cursor


class APP:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ClienteController().cliente_controller)
        self.app.register_blueprint(ProdutoController().produto_controller)
        self.app.register_blueprint(ContratoController().contrato_controller)
        self.app.register_blueprint(ParcelaController().parcela_controller)
        self.app.register_blueprint(ItemProdutoController().item_produto_controller)
        Cursor().initTables()

    def run(self):
        return self.app.run(debug=True)


if __name__ == "__main__":
    APP().run()

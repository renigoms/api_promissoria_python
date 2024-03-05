import psycopg2
from flask import request
from flask.sansio.blueprints import Blueprint

from Modules.Produto.DAO import DAOProduto
from Modules.Produto.model import Produto
from Services.Exceptions import NullException, IDException, NotAlterException, ProductException, ForeingKeyException, \
    ReactiveException
from Util.ServerUtils import ResponseUtils


class ProdutoController:
    produto_controller = Blueprint('produto_controller', __name__)
    module_name = 'produto'

    @staticmethod
    @produto_controller.route(f'/{module_name}/', methods=['GET'])
    def get_all_controller():
        search = request.args.get('search')
        return ResponseUtils.get_response_busca(DAOProduto.get_all)\
            if search is None else ResponseUtils.get_response_busca(DAOProduto.get_by_search(search))

    @staticmethod
    @produto_controller.route(f'/{module_name}/', methods=['POST'])
    def create_controller():
        try:
            data = request.json
            return ResponseUtils.generate_response("Produto Cadastrado com Sucesso", 200) \
                if DAOProduto.post_create(Produto(**data)) \
                else ResponseUtils.generate_response("Erro ao adicionar produto", 400)

        except psycopg2.errors.UniqueViolation as e:
            return ResponseUtils.generate_response("Esse produto já existe", 400)
        except NullException as e:
            return ResponseUtils.generate_response("Alguns itens obrigatorios não foram preenchidos", 400)
        except IDException as e:
            return ResponseUtils.generate_response("O ID é adicionado automáticamente, não sendo permitida"
                                                   "a sua adição manual!", 400)
        except ReactiveException as e:
            return ResponseUtils.generate_response("Produto Reativado !", 200)
        except Exception as e:
            print(e)
            return ResponseUtils.generate_response("Erro ao adicionar produto!", 400)

    @staticmethod
    @produto_controller.route(f'/{module_name}/<id>', methods=['PUT'])
    def update_controller(id: str):
        try:
            return ResponseUtils.generate_response("Produto atualizado com sucesso!!!", 200) \
                if DAOProduto.put_update(Produto(**request.json), id) \
                else ResponseUtils.generate_response("Erro durante a tentativa de alteração !!", 400)
        except IDException as e:
            return ResponseUtils.generate_response("O id deve ser passado obrigatoriamente !!!", 400)
        except NotAlterException as e:
            return ResponseUtils.generate_response("O id não pode ser modificado !!!", 400)
        except ProductException as e:
            return ResponseUtils.generate_response("O produto selecionado não existe na base!", 400)
        except Exception as e:
            print(e)
            return ResponseUtils.generate_response("Erro durante a tentativa de alteração !!!", 400)

    @staticmethod
    @produto_controller.route(f'/{module_name}/<id>', methods=["DELETE"])
    def delete_controller(id: str):
        try:
            return ResponseUtils.generate_response("Produto deletado com sucesso!", 200) \
                if DAOProduto.delete(id) \
                else ResponseUtils.generate_response("Erro ao deletar esse Produto !!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response("Você precisa fornecer o ID do cliente "
                                                   "que quer deletar", 400)
        except ForeingKeyException as e:
            return ResponseUtils.generate_response("Não foi possivel excluir o produto,"
                                                   " pois ele possui um ou mais contratos ativos !!", 400)
        except ProductException as e:
            return ResponseUtils.generate_response("O produto selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response("Erro ao deletar esse cliente !!!", 400)
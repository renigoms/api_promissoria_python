import psycopg2
from flask import request
from flask.sansio.blueprints import Blueprint

from Modules.Cliente.DAO import DAOCliente
from Modules.Cliente.model import Cliente
from Services.Exceptions import NullException, IDException, NotAlterException, ClientException, ForeingKeyException, \
    ReactiveException
from Util.DaoUltil import UtilGeral
from Util.ServerUtils import ResponseUtils


class ClienteController:
    cliente_controller = Blueprint('cliente_controller', __name__)
    module_name = 'cliente'

    @staticmethod
    @cliente_controller.route(f'/{module_name}/', methods=['GET'])
    def get_all_controller():
        search = request.args.get('search')
        return ResponseUtils.get_response_busca(DAOCliente.get_all) \
            if search is None else ResponseUtils.get_response_busca(DAOCliente.get_by_search(search))

    @staticmethod
    @cliente_controller.route(f'/{module_name}/', methods=['POST'])
    def create_controller():
        global data
        try:
            data = request.json
            if UtilGeral.is_requered_itens_null(data, DAOCliente.REQUERED_ITEMS):
                raise NullException()
            return ResponseUtils.generate_response("Cliente Cadastrado com Sucesso", 200) \
                if DAOCliente.post_create(Cliente(**data)) \
                else ResponseUtils.generate_response("Erro ao adicionar cliente", 400)
        except psycopg2.errors.UniqueViolation as e:
            return ResponseUtils.generate_response("Esse cliente já existe", 400)
        except psycopg2.errors.StringDataRightTruncation as e:
            return ResponseUtils.generate_response("O nome, o cpf, o email ou o telefone estão muito extensos!", 400)
        except ReactiveException as e:
            return ResponseUtils.generate_response("Cliente Reativado !", 200)
        except NullException as e:
            return ResponseUtils.generate_response(
                ResponseUtils.requered_message(
                    DAOCliente.REQUERED_ITEMS, data
                    ), 400)
        except IDException as e:
            return ResponseUtils.generate_response("O ID é adicionado automáticamente, não sendo permitida"
                                                   "a sua adição manual!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao adicionar cliente: {e}", 400)

    @staticmethod
    @cliente_controller.route(f'/{module_name}/<id>', methods=['PUT'])
    def update_controller(id: str):
        try:
            return ResponseUtils.generate_response("Cliente atualizado com sucesso!!!", 200) \
                if DAOCliente.put_update(Cliente(**request.json), id) \
                else ResponseUtils.generate_response("Erro durante a tentativa de alteração !!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response("O id deve ser passado obrigatoriamente !!!", 400)
        except NotAlterException as e:
            return ResponseUtils.generate_response("O id não pode ser modificado !!!", 400)
        except ClientException as e:
            return ResponseUtils.generate_response("O cliente selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response("Erro durante a tentativa de alteração !!!", 400)

    @staticmethod
    @cliente_controller.route(f'/{module_name}/<id>', methods=["DELETE"])
    def delete_controller(id: str):
        try:
            return ResponseUtils.generate_response("Cliente deletado com sucesso!", 200) \
                if DAOCliente.delete(id) \
                else ResponseUtils.generate_response("Erro ao deletar esse cliente !!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response("Você precisa fornecer o ID do cliente "
                                                   "que quer deletar", 400)
        except ForeingKeyException as e:
            return ResponseUtils.generate_response("Não foi possivel excluir o cliente,"
                                                   " pois ele possui um ou mais contratos ativos !!", 400)
        except ClientException as e:
            return ResponseUtils.generate_response("O cliente selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response("Erro ao deletar esse cliente !!!", 400)

import sys

import psycopg2
from flask import jsonify, request
from flask.sansio.blueprints import Blueprint

from Modules.Cliente.DAO import DAOCliente
from Modules.Cliente.model import Cliente
from Services.Exceptions import NullException, IDException, NotAlterException, ClientException
from Util.ServerUtils import ResponseUtils


class ClienteController:
    cliente_controller = Blueprint('cliente_controller', __name__)
    module_name = 'cliente'

    @staticmethod
    @cliente_controller.route(f'/{module_name}/', methods=['GET'])
    def get_all_controller():
        return ResponseUtils.get_response_busca(DAOCliente.get_all)

    @staticmethod
    @cliente_controller.route(f'/{module_name}/<id>/', methods=['GET'])
    def get_by_id_controller(id: str):
        return ResponseUtils.get_response_busca(DAOCliente.get_by_id(id))

    @staticmethod
    @cliente_controller.route(f'/{module_name}/cpf/<cpf>/', methods=['GET'])
    def get_by_cpf_controller(cpf: str):
        return ResponseUtils.get_response_busca(DAOCliente.get_by_cpf(cpf))

    @staticmethod
    @cliente_controller.route(f'/{module_name}/', methods=['POST'])
    def create_controller():
        try:
            data = request.json
            return ResponseUtils.generate_response("Cliente Cadastrado com Sucesso", 200) \
                if DAOCliente.post_create(Cliente(**data)) \
                else ResponseUtils.generate_response("Erro ao adicionar cliente", 400)
        except psycopg2.DatabaseError as e:
            return ResponseUtils.generate_response("Esse cliente já existe", 400)
        except NullException as e:
            return ResponseUtils.generate_response("Alguns itens obrigatorios não foram preenchidos", 400)
        except IDException as e:
            return ResponseUtils.generate_response("O ID é adicionado automáticamente, não sendo permitida"
                                                   "a sua adição manual!", 400)
        except Exception as e:
            return ResponseUtils.generate_response("Erro ao adicionar cliente", 400)

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
        except psycopg2.errors.ForeignKeyViolation as e:
            return ResponseUtils.generate_response("Não foi possivel excluir o cliente,"
                                                   " pois ele possui um ou mais contratos ativos !!", 400)
        except ClientException as e:
            return ResponseUtils.generate_response("O cliente selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response("Erro ao deletar esse cliente !!!", 400)

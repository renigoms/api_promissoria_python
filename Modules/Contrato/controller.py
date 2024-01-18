import psycopg2.errors
from flask import request
from flask.sansio.blueprints import Blueprint

from Modules.Contrato.DAO import DAOContrato
from Modules.Contrato.model import Contrato
from Services.Exceptions import NullException, ParcelaEmAbertoExcerption, IDException
from Util.ServerUtils import ResponseUtils


class ContratoController:
    contrato_controller = Blueprint('contrato_controller', __name__)
    modulo_name = 'contrato'

    @staticmethod
    @contrato_controller.route(f'/{modulo_name}/', methods=['GET'])
    def get_all_controller():
        return ResponseUtils.get_response_busca(DAOContrato.get_all)

    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/<id>", methods=['GET'])
    def get_by_id(id:str):
        return ResponseUtils.get_response_busca(DAOContrato.get_by_id(id))

    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/cpf_cliente/<cpf>/", methods=['GET'])
    def get_cpf_cliente(cpf:str):
        return ResponseUtils.get_response_busca(DAOContrato.get_by_cliente_cpf(cpf))

    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/", methods=['POST'])
    def create_controller():
        try:
            data = request.json
            return ResponseUtils.generate_response("Contrato gerado com sucesso !!", 200)\
                if DAOContrato.post_create(Contrato(**data))\
                else ResponseUtils.generate_response("Erro ao gerar contrato !!", 400)
        except NullException() as e:
            return ResponseUtils.generate_response("Alguns itens obrigatórios não foram preenchidos!!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao Gerar Contrato: {e}")


    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/<id>/", methods=['DELETE'])
    def delete_controller(id:str):
        try:
            return ResponseUtils.generate_response("Contrato delatado com sucesso!!", 200) \
                if DAOContrato.delete(id) \
                else ResponseUtils.generate_response("Erro ao deletar o contrato !!", 400)
        except ParcelaEmAbertoExcerption as e:
            return ResponseUtils.generate_response(f"Ainda há parcelas não pagas ligadas à esse contrato!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response(f"O id deve obrigatoriamente ser passado!!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao deletar o contrato: {e}")
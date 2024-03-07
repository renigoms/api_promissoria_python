import sys
from flask import request
from flask.sansio.blueprints import Blueprint
from Modules.Contrato.DAO import DAOContrato
from Modules.Contrato.model import Contrato
from Services.Exceptions import NullException, ParcelaEmAbertoExcerption, IDException, AutoValueException, \
    ContractException, ClientException, ProductException
from Util.DaoUltil import UtilGeral
from Util.ServerUtils import ResponseUtils


class ContratoController:
    contrato_controller = Blueprint('contrato_controller', __name__)
    modulo_name = 'contrato'

    @staticmethod
    @contrato_controller.route(f'/{modulo_name}/', methods=['GET'])
    def get_all_controller():
        search = request.args.get('search')
        return ResponseUtils.get_response_busca(DAOContrato.get_all) \
            if search is None else ResponseUtils.get_response_busca(DAOContrato.get_by_search(search))

    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/", methods=['POST'])
    def create_controller():
        global data
        try:
            data = request.json
            if UtilGeral.is_auto_itens_not_null(data, DAOContrato.auto_items):
                raise AutoValueException
            if UtilGeral.is_requered_itens_null(data, DAOContrato.requered_items):
                raise NullException
            return ResponseUtils.generate_response("Contrato gerado com sucesso !!", 200) \
                if DAOContrato.post_create(Contrato(**data)) \
                else ResponseUtils.generate_response("Erro ao gerar contrato !!", 400)
        except NullException as e:
            return ResponseUtils.generate_response(ResponseUtils.requered_message(DAOContrato.requered_items, data), 400)
        except AutoValueException as e:
            return ResponseUtils.generate_response(
                ResponseUtils.auto_items_message(DAOContrato.auto_items, data), 400)
        except ClientException as e:
            return ResponseUtils.generate_response("O cliente selecionado não existe na base!", 400)
        except ProductException as e:
            return ResponseUtils.generate_response("O produto selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro inesperado ao Gerar Contrato: {e}", 400)

    @staticmethod
    @contrato_controller.route(f"/{modulo_name}/<id>/", methods=['DELETE'])
    def delete_controller(id: str):
        try:
            return ResponseUtils.generate_response("Contrato delatado com sucesso!!", 200) \
                if DAOContrato.delete(id) \
                else ResponseUtils.generate_response("Erro ao deletar o contrato !!", 400)
        except ParcelaEmAbertoExcerption as e:
            return ResponseUtils.generate_response(f"Ainda há parcelas não pagas ligadas à esse contrato!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response(f"O id deve obrigatoriamente ser passado!!", 400)
        except ContractException as e:
            return ResponseUtils.generate_response("O contrato selecionado não existe na base !", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao deletar o contrato: {e}", 400)

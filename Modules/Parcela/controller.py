from flask import request
from flask.sansio.blueprints import Blueprint

from Modules.Contrato.model import Contrato
from Modules.Parcela.DAO import DAOParcela
from Modules.Parcela.model import Parcela
from Services.Exceptions import IDException, ParcelasDefinidasException, NotAlterException, ContractException, \
    InstallmentDateException
from Util.ServerUtils import ResponseUtils


class ParcelaController:
    parcela_controller = Blueprint('parcela_controller', __name__)
    modulo_name = "parcela"

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/<id_contrato>", methods=["GET"])
    def get_by_id_contrato_controller(id_contrato: str):
        return ResponseUtils.get_response_busca(DAOParcela.get_by_id_contrato(id_contrato))

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/<id_contrato>/<data_pag>", methods=["GET"])
    def get_by_data_pag_controller(id_contrato: str, data_pag: str):
        return ResponseUtils.get_response_busca(DAOParcela.get_data_pag(id_contrato, data_pag))

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/", methods=["POST"])
    def create_controller():
        try:
            data = request.json
            return ResponseUtils.generate_response("Parcelas geradas com sucesso!!", 200) \
                if DAOParcela.post_create(Contrato(**data)) \
                else ResponseUtils.generate_response("Erro ao criar as parcealas!!", 400)
        except IDException as e:
            return ResponseUtils.generate_response("Você deve passar apenas o id do contrato", 400)
        except ParcelasDefinidasException as e:
            return ResponseUtils.generate_response("As parcelas desse contrato já foram definidas !!", 400)
        except ContractException as e:
            return ResponseUtils.generate_response("O contrato selecionado não existe na base!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao criar parcelas: {e}", 400)

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/<id_contrato>/<data_pag>", methods=["PUT"])
    def update_controller(id_contrato: str, data_pag: str):
        try:
            data = request.json
            return ResponseUtils.generate_response("Update realizado com sucesso !!!", 200) \
                if DAOParcela.put_update(Parcela(**data), id_contrato, data_pag) \
                else ResponseUtils.generate_response("Falha no Update !!", 400)
        except NotAlterException as e:
            return ResponseUtils.generate_response("Você deve alterar apenas o status !!", 400)
        except IDException as e:
            return ResponseUtils.generate_response(f"Você deve passar o id do contrato e"
                                                   f"a data da parcela que deseja alterar", 400)
        except ContractException as e:
            return ResponseUtils.generate_response("O contrato selecionado não existe na base!", 400)
        except InstallmentDateException as e:
            return ResponseUtils.generate_response("Não existe uma parcela nesse contrato que contenha essa data!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Falha no Update: {e}", 400)

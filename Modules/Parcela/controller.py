from flask import request
from flask.sansio.blueprints import Blueprint

from Modules.Contrato.model import Contrato
from Modules.Parcela.DAO import DAOParcela
from Modules.Parcela.model import Parcela
from Services.Exceptions import IDException, ParcelasDefinidasException, NotAlterException, ContractException, \
    ParcelaException
from Util.ServerUtils import ResponseUtils


class ParcelaController:
    parcela_controller = Blueprint('parcela_controller', __name__)
    modulo_name = "parcela"

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/", methods=['GET'])
    def get_controller():
        id_contrato = request.args.get('id_contrato')
        data_pag = request.args.get('data_pag')

        if id_contrato is not None and data_pag is None:
            return ResponseUtils.get_response_busca(DAOParcela.get_by_id_contrato(id_contrato))

        if id_contrato is not None and data_pag is not None:
            return ResponseUtils.get_response_busca(DAOParcela.get_data_pag(id_contrato, data_pag))

        return ResponseUtils.get_response_busca([])

    @staticmethod
    @parcela_controller.route(f"/{modulo_name}/<id_contrato>/data_pag/<data_pag>", methods=["PUT"])
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
        except ParcelaException as e:
            return ResponseUtils.generate_response("Não existe uma parcela nesse contrato que contenha essa data!", 400)
        except Exception as e:
            return ResponseUtils.generate_response(f"Falha no Update: {e}", 400)

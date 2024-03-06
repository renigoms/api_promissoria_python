import sys
from flask import jsonify


class ResponseUtils:
    @staticmethod
    def get_response_busca(list_object):
        try:
            result = [object_item.to_dict() for object_item in list_object]
            return ResponseUtils.generate_response(result, 200)
        except Exception as e:
            return ResponseUtils.generate_response(f"Erro ao realizar a busca: {sys.exc_info()}", 500)

    @staticmethod
    def generate_response(result, status_code):
        respose = jsonify(result)
        respose.status_code = status_code
        return respose

    @staticmethod
    def requered_message(list_requered:list, json_request:dict) -> str:
        itens = [None, '', "", """""", 0, 0.0]

        for camp in list_requered:
            try:
                if itens.__contains__(json_request[camp]):
                    return f"O campo {camp} é obrigatório !"
            except KeyError as e:
                return f"O campo {camp} é obrigatório !"

        return "Campo diferente dos aceitos pelo sistema detectado !"

    @staticmethod
    def auto_items_message(list_auto_items:str, json_request: dict) -> str:
        for camp in list_auto_items:
            try:
                teste = json_request[camp]
                return f"O campo {camp} é definido automaticamente. Sua adição manual não é permitida !"
            except KeyError as e:
                continue

        return "Campo diferente dos aceitos pelo sistema detectado !"

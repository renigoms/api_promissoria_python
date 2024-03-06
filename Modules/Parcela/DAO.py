import datetime as dt
import sys

from dateutil.relativedelta import relativedelta

from Modules.Parcela.SQL import SQLParcela
from Modules.Parcela.model import Parcela
from Services.Connect_db_pg import Cursor
from Services.Exceptions import IDException, NotAlterException, ParcelaException, \
    ContractException
from Util.DaoUltil import UtilGeral


class DAOParcela:
    create_table = SQLParcela.CREATE_TABLE

    get_by_id_contrato = lambda id: UtilGeral.getSelectDictParcela(SQLParcela.SELECT_BY_ID_CONTRATO, id)

    get_data_pag = lambda id_contrato, data_pag: UtilGeral.getSelectDictParcela(
        SQLParcela.SELECT_BY_ID_CONTRATO_AND_DATA_PAG,
        id_contrato, data_pag)

    @staticmethod
    def create_parcela(valor_contrato: float, num_parcelas: int, id_contrato: int) -> int:

        cont_sucess_parcels = 0

        #     data atual com salto de um mês
        date_today = dt.datetime(dt.datetime.now().year, dt.datetime.now().month + 1, dt.datetime.now().day)

        # Calculo do valor de cada parcela
        valor_parcela = lambda x, y: x / y

        #     Definição das parcelas de acordo com a quantidade definida no contrato
        count = 0

        while count < num_parcelas:
            if Cursor().execute(SQLParcela.CREATE, id_contrato, valor_parcela(
                    valor_contrato, num_parcelas), date_today.strftime("%d-%m-%Y")):
                date_today = date_today + relativedelta(months=+1)
                cont_sucess_parcels += 1
            count += 1

        return cont_sucess_parcels

    AUTO_ITENS = SQLParcela.AUTO_ITEMS

    _is_paga_only = lambda parcela: UtilGeral.is_auto_itens_not_null(parcela.__dict__, DAOParcela.AUTO_ITENS)

    @staticmethod
    def put_update(parcela: Parcela, id_contrato: str, data_pag: str):
        try:
            if (id_contrato is None or id_contrato == ""
                    or data_pag is None or data_pag == ""):
                raise IDException()

            if DAOParcela._is_paga_only(parcela):
                raise NotAlterException()

            if UtilGeral.is_not_contract_exists(id_contrato):
                raise ContractException()

            if UtilGeral.is_not_parcels_exists(id_contrato, data_pag):
                raise ParcelaException()

            old_parcela = DAOParcela.get_data_pag(id_contrato, data_pag)

            paga = UtilGeral.get_Val_Update(old_parcela[0].paga, parcela.paga)

            return Cursor().execute(SQLParcela.UPDATE, paga, id_contrato, data_pag)

        except NotAlterException as e:
            raise e
        except IDException as e:
            raise e
        except ContractException as e:
            raise e
        except ParcelaException as e:
            raise e
        except Exception as e:
            print(f"Erro durante o update: {e}")
            print(sys.exc_info())
            return False

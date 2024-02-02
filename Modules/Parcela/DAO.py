import sys
import traceback

from Modules.Contrato.SQL import SQLContrato
from Modules.Contrato.model import Contrato
from Modules.Parcela.SQL import SQLParcela
from Modules.Parcela.model import Parcela
from Services.Connect_db_pg import Cursor

from Services.Exceptions import IDException, ParcelasDefinidasException, NotAlterException, InstallmentDateException, \
    ContractException
from Util.DaoUltil import UtilGeral
import datetime as dt

from Util.SQLGeral import SQLGeral


class DAOParcela:
    create_table = SQLParcela.CREATE_TABLE

    get_by_id_contrato = lambda id: UtilGeral.getSelectDictParcela(SQLParcela.SELECT_BY_ID_CONTRATO, id)

    get_data_pag = lambda id_contrato, data_pag: UtilGeral.getSelectDictParcela(
        SQLParcela.SELECT_BY_ID_CONTRATO_AND_DATA_PAG,
        id_contrato, data_pag)

    @staticmethod
    def _is_no_alter_contrato(contrato: Contrato) -> bool:
        return (contrato.id_produto is not None
                or contrato.id_cliente is not None
                or contrato.num_parcelas != 0
                or contrato.data_criacao is not None
                or contrato.valor is not None
                or contrato.qnt_produto > 1
                or contrato.descricao is not None
                or contrato.parcelas_definidas is not None)

    @staticmethod
    def post_create(contrato: Contrato):
        try:
            from Services.Connect_db_pg import Cursor
            if DAOParcela._is_no_alter_contrato(contrato):
                raise IDException()

            contratoList = UtilGeral.getSelectDictContrato(SQLParcela.SELECT_CONTRATO, contrato.id)

            if contratoList[0].parcelas_definidas:
                raise ParcelasDefinidasException()

            cont_sucesso = 0

            cont = 0

            dateToday = dt.datetime(dt.datetime.now().year, dt.datetime.now().month + 1, dt.datetime.now().day)

            valor = lambda x, y: x / y

            while cont < contratoList[0].num_parcelas:
                if Cursor().execute(SQLParcela.CREATE,
                                    contrato.id, valor(contratoList[0].valor, contratoList[0].num_parcelas),
                                    dateToday.strftime("%d-%m-%Y")):
                    dateToday = dt.datetime(dateToday.year, dateToday.month + 1, dateToday.day)
                    cont_sucesso += 1
                cont += 1

            return Cursor().execute(SQLContrato.UPDATE_PARCELAS_DEFINIDAS, contrato.id) \
                if cont_sucesso == contratoList[0].num_parcelas else False

        except IDException as e:
            raise e
        except ParcelasDefinidasException as e:
            raise e
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            print(sys.exc_info())
            traceback.print_exc()
            return False

    @staticmethod
    def _is_not_alter_parcela(parcela: Parcela) -> bool:
        return (parcela.id is not None
                or parcela.id_contrato is not None
                or parcela.valor is not None
                or parcela.data_pag is not None
                or parcela.status is None)

    @staticmethod
    def _is_installment_date_exists(dataPag: str):
        getParcela = UtilGeral.getSelectDictParcela(SQLParcela.SELECT_BY_DATA_PAG, dataPag)
        return len(getParcela) == 0

    @staticmethod
    def put_update(parcela: Parcela, id_contrato: str, data_pag: str):
        try:
            if (id_contrato is None or id_contrato == ""
                    or data_pag is None or data_pag == ""):
                raise IDException()

            if DAOParcela._is_not_alter_parcela(parcela):
                raise NotAlterException()

            if DAOParcela._is_installment_date_exists(data_pag):
                raise InstallmentDateException()

            if UtilGeral.is_contract_exists(id_contrato):
                raise ContractException()

            old_parcela = DAOParcela.get_data_pag(id_contrato, data_pag)

            status = UtilGeral.get_Val_Update(old_parcela[0].status, parcela.status)

            return Cursor().execute(SQLParcela.UPDATE, status, id_contrato, data_pag)

        except NotAlterException as e:
            raise e
        except IDException as e:
            raise e
        except ContractException as e:
            raise e
        except InstallmentDateException as e:
            raise e
        except Exception as e:
            print(f"Erro durante o update: {e}")
            print(sys.exc_info())
            return False

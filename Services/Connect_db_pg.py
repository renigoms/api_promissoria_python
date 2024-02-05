import sys

import psycopg2
import psycopg2 as pg


class Connection_db:
    def __init__(self, **dicio):
        self.dicio = dicio

    def __enter__(self):
        try:
            self.getConnection = pg.connect(**self.dicio)

            self.cursor = self.getConnection.cursor()

            return self.cursor
        except:
            print(f"Erro ao conectar com o banco de dados: "
                  f"{sys.exc_info()}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.getConnection.commit()


class Cursor:
    def __init__(self):
        self.dicio2 = dict(
            database="promissorias_fbd",
            host="localhost",
            user="postgres",
            password="rngazrcb",
            port="5432"
        )

    def execute(self, query, *args):
        try:
            with Connection_db(**self.dicio2) as cursor:
                cursor.execute(query, tuple(args))
                return True
        except psycopg2.errors.UniqueViolation as e:
            raise e
        except psycopg2.errors.ForeignKeyViolation as e:
            raise e
        except:
            print(f"Erro durante a execução da Query: {sys.exc_info()}")
            return False

    def query(self, query, *args):
        try:
            with (Connection_db(**self.dicio2) as cursor):
                cursor.execute(query, tuple(args))
                result_cursor = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                return [dict(zip(cols, i)) for i in result_cursor]
        except Exception as e:
            print(f"Erro durante a execução da Query: {sys.exc_info()}")
            return False

    def initTables(self):
        try:
            from Modules.Cliente.DAO import DAOCliente
            from Modules.Produto.DAO import DAOProduto
            from Modules.Contrato.DAO import DAOContrato
            from Modules.Parcela.DAO import DAOParcela

            self.execute(DAOCliente.create_table)
            self.execute(DAOProduto.create_table)
            self.execute(DAOContrato.create_table)
            self.execute(DAOParcela.create_table)
            return True
        except:
            print(f"Falha ao iniciar as tabelas: {sys.exc_info()}")
            return False

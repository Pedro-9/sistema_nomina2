from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Puesto:
    def __init__(self) -> None:
        pass


    @staticmethod
    def get_fecha():
        ahora = datetime.now()
        return str(ahora.date())

    @staticmethod
    def execute_query(query, params=None, fetchall=False):
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetchall:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        
    @staticmethod
    def execute_commit(query, params=None):
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute(query, params)
            mysql.connection.commit()
            return True
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    def get_puestos(self):
        query = 'SELECT * FROM puestos'
        return self.execute_query(query, fetchall=True)

  
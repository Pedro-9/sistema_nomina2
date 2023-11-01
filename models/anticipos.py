from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Anticipo:
    def __init__(self):
        self.id_anticipo = ""

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

    def get_anticipos(self):
            query = '''SELECT a.id_anticipo, u.usuario as id_usuario, a.fecha_atencion, a.fecha_pago, a.descripcion, a.monto
                        FROM anticipos a
                        INNER JOIN usuarios u ON a.id_usuario = u.id_usuario'''
            return self.execute_query(query, fetchall=True)
        
    def insert_anticipo(self, fecha_atencion, fecha_pago, descripcion, id_usuario):
        query = '''
            INSERT INTO anticipos (fecha_atencion, fecha_pago, descripcion, estado, id_usuario)
            VALUES (%s, %s, %s, 0, %s)
            '''
        params = (fecha_atencion, fecha_pago, descripcion, id_usuario)
        return self.execute_commit(query, params)

    
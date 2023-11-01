from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Prestamo:
    def __init__(self):
        self.id_prestamo = ""

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

    def get_prestamos(self):
        query = '''SELECT p.id_prestamo, u.usuario as id_usuario_solicita, p.fecha_atencion, p.descripcion, p.plazo_meses, 
        ROUND((p.monto / p.plazo_meses),2) as pago_mensual,p.monto
                    FROM prestamos p
                    INNER JOIN usuarios u ON p.id_usuario_solicita = u.id_usuario'''
        return self.execute_query(query, fetchall=True)

    def get_prestamo(self, id_prestamo):
        query = 'SELECT * FROM prestamos WHERE id_prestamo = %s'
        params = (id_prestamo,)
        return self.execute_query(query, params=params)
    
    def insert_prestamo(self, fecha_atencion, descripcion, plazo_meses, monto, id_usuario_solicita, id_usuario_atiende):
        query = '''
        INSERT INTO prestamos (fecha_atencion, descripcion, plazo_meses, monto, estado, id_usuario_solicita, id_usuario_atiende)
        VALUES (%s, %s, %s, %s, 0, %s, %s)
        '''
        params = (fecha_atencion, descripcion, plazo_meses, monto, id_usuario_solicita, id_usuario_atiende)
        return self.execute_commit(query, params)

    
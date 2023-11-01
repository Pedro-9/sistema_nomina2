from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Nominass:
    def __init__(self):
        self.id_nomina = ""

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

    def get_nominas(self):
        query = ''' SELECT n.id_nomina, concat(e.nombre, ' ', e.apellido) as id_empleado, n.fecha, n.       horas_trabajadas, n.horas_extra, n.ausencia_dias,  n.dias, n.venta_total, n.comisiones, n.bonificaciones
                    FROM nominas n 
                    INNER JOIN empleados e ON n.id_empleado = e.id_empleado'''
        return self.execute_query(query, fetchall=True)

    def insert_nomina(self, id_empleado, fecha, ausencia_dias, horas_extra, venta_total):
        query = '''
            INSERT INTO nominas (id_empleado, fecha, ausencia_dias, horas_extra, venta_total, estado)
            VALUES (%s, %s, %s, %s, %s, 0)
        '''
        params = (id_empleado, fecha, ausencia_dias, horas_extra, venta_total)
        return self.execute_commit(query, params)

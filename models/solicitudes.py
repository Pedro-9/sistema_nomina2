from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger

class Solicitude:
    def __init__(self):
        self.id = 0
        self.id_solicitud = ""

    def getFecha(self):
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

    def get_solicitudes(self):
        query = 'SELECT * FROM solicitud_permisos where estado = %s'
        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_solicitud(self, id_rol):
        query = 'SELECT * FROM solicitud_permisos where estado = %s AND id_solicitud = %s'
        params = ('0', id_rol)
        return self.execute_query(query, params=params)

    def insert_solicitud(self, nombre_rol):
        query = '''
                    INSERT INTO solicitud_permisos (
                    dias_solicitadas, inicio_permiso, fin_permiso, descripcion, retorno_laboral, id_usuario_atiende, id_usuario_solicita, fecha_registro, estado
                    estado) VALUES (%s, %s)'''
        params = (nombre_rol, '0')
        return self.execute_commit(query, params)
    
    def update_solicitud(self, nombre_rol, id_rol):
        query = '''
            UPDATE solicitud_permisos
            SET nombre_rol = %s
            WHERE id_solicitud = %s
        '''
        params = (nombre_rol, id_rol)
        return self.execute_commit(query, params)
    
    def delete_solicitud(self, id_rol, estado):
        query = '''
            UPDATE solicitud_permisos
            SET estado = %s
            WHERE id_solicitud = %s
        '''
        params = (estado, id_rol)
        return self.execute_commit(query, params)
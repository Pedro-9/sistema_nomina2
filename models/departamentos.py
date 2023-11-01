from db import mysql
import traceback
from utils.Logger import Logger

class Departamento:
    def __init__(self):
        self.id_departamento = ""

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

    def get_departamentos(self):
        query = 'SELECT * FROM departamentos where estado = %s'
        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_departamento(self, id_departamento):
        query = 'SELECT * FROM departamentos where estado = %s AND id_departamento = %s'
        params = ('0', id_departamento)
        return self.execute_query(query, params=params)

    def insert_departamento(self, nombre_departamento, id_usuario):
        query = '''
                    INSERT INTO departamentos (
                    nombre,
                    estado, id_usuario) VALUES (%s, %s, %s)'''
        params = (nombre_departamento, '0', id_usuario)
        return self.execute_commit(query, params)
    
    def update_departamento(self, nombre_departamento, id_usuario, id_departamento):
        query = '''
            UPDATE departamentos
            SET nombre = %s, id_usuario = %s
            WHERE id_departamento = %s
        '''
        params = (nombre_departamento, id_usuario, id_departamento)
        return self.execute_commit(query, params)
    
    def delete_departamento(self, id_departamento, estado):
        query = '''
            UPDATE departamentos
            SET estado = %s
            WHERE id_departamentso = %s
        '''
        params = (estado, id_departamento)
        return self.execute_commit(query, params)
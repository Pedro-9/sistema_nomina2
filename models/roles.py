from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Rol:
    def __init__(self):
        self.id_rol = ""

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

    def get_roles(self):
        query = 'SELECT * FROM roles where estado = %s'
        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_rol(self, id_rol):
        query = 'SELECT * FROM roles where estado = %s AND id_rol = %s'
        params = ('0', id_rol)
        return self.execute_query(query, params=params)

    def insert_rol(self, nombre_rol):
        query = '''
                    INSERT INTO roles (
                    nombre_rol,
                    estado) VALUES (%s, %s)'''
        params = (nombre_rol, '0')
        return self.execute_commit(query, params)
    
    def update_rol(self, nombre_rol, id_rol):
        query = '''
            UPDATE roles
            SET nombre_rol = %s
            WHERE id_rol = %s
        '''
        params = (nombre_rol, id_rol)
        return self.execute_commit(query, params)
    
    def delete_rol(self, id_rol, estado):
        query = '''
            UPDATE roles
            SET estado = %s
            WHERE id_rol = %s
        '''
        params = (estado, id_rol)
        return self.execute_commit(query, params)
from datetime import datetime
from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger
from models.usuario import Usuario

user = Usuario()


class Empresa:
    def __init__(self):
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

    def insert_empresa(self, nombre_empresa):
        if self.existe_empresa(nombre_empresa) == None:
            query = '''
                        INSERT INTO empresas (
                        nombre_empresa,
                        fecha_ingreso,
                        estado, id_usuario) VALUES (%s, %s, %s, %s)'''
            params = (nombre_empresa, self.get_fecha(), '0', '1')
            return self.execute_commit(query, params)
        else:
            return False
        
    def existe_empresa(self, nombre_empresa):
        query = '''
            SELECT * FROM empresas WHERE nombre_empresa = %s 
            AND estado = %s '''
        params = (nombre_empresa, '0')
        return self.execute_query(query, params=params)

    def get_empresas(self):
        query = 'SELECT * FROM empresas where estado = %s order by id_empresa desc'
        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_empresa(self, id_empresa):
        query = '''
            SELECT *
            FROM empresas
            WHERE id_empresa = %s AND estado = %s
        '''
        params = (id_empresa, '0')
        return self.execute_query(query, params)

    def update_empresa(self, nombre_empresa, id_empresa):
        query = '''
            UPDATE empresas
            SET nombre_empresa = %s
            WHERE id_empresa = %s
        '''
        params = (nombre_empresa, id_empresa)
        return self.execute_commit(query, params)

    def update_id_usuario(self, id_usuario, id_empresa):
        query = '''
            UPDATE empresas
            SET id_usuario = %s
            WHERE id_empresa = %s
        '''
        params = (id_usuario, id_empresa)
        return self.execute_commit(query, params)

    def delete_empresa(self, id_empresa, estado):
        query = '''
            UPDATE empresas
            SET estado = %s, fecha_retiro = %s
            WHERE id_empresa = %s
        '''
        params = (estado, self.get_fecha(), id_empresa)
        return self.execute_commit(query, params)


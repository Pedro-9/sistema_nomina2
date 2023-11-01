from datetime import datetime
from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger


class Empleado:
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

    def insert_empleado(self, nombre_empresa):
        if self.existe_empresa(nombre_empresa) == None:
            query = '''
                        INSERT INTO empleados (
                        nombre_empresa,
                        fecha_ingreso,
                        estado, id_usuario) VALUES (%s, %s, %s, %s)'''
            params = (nombre_empresa, self.get_fecha(), '0', '1')
            return self.execute_commit(query, params)
        else:
            return False
        
    def existe_empleado(self, nombre_empresa):
        query = '''
            SELECT * FROM empresas WHERE nombre_empresa = %s 
            AND estado = %s '''
        params = (nombre_empresa, '0')
        return self.execute_query(query, params=params)

    def get_empleados(self):
        query = '''
        select em.id_empleado, em.nombre, em.apellido, em.dpi, em.nit, em.igss, 
        em.direccion, em.telefono, em.correo, em.genero, emp.nombre_empresa, p.puesto, em.estado
        from empleados as em
        inner join puestos as p
        on em.id_puesto = p.id
        inner join empresas as emp
        on emp.id_empresa = em.id_empresa 
        where em.estado = %s order by id_empleado desc'''
        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_empleado(self, id_empresa):
        query = '''
            SELECT *
            FROM empresas
            WHERE id_empresa = %s AND estado = %s
        '''
        params = (id_empresa, '0')
        return self.execute_query(query, params)

    def update_empleado(self, nombre_empresa, id_empresa):
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

    def delete_empleado(self, id_empresa, estado):
        query = '''
            UPDATE empresas
            SET estado = %s, fecha_retiro = %s
            WHERE id_empresa = %s
        '''
        params = (estado, self.get_fecha(), id_empresa)
        return self.execute_commit(query, params)


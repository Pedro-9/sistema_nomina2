from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, password) -> None:
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


class Usuario:
    def __init__(self):
        self.id = 0
        self.id_rol = 0
        self.ultimo_id = ''

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
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    def insert_usuario(self, usuario, password, id_rol, id_empresa):
        try:
            password_hash = generate_password_hash(password)
            if self.existe_usuario(usuario) == None:
                with mysql.connection.cursor() as cursor:
                    cursor.execute('''
                                INSERT INTO usuarios(
                                usuario, password, f_registro,
                                f_modificacion, estado, id_rol, id_empresa) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                   (usuario, password_hash, self.getFecha(), self.getFecha(), '0', id_rol, id_empresa))
                mysql.connection.commit()
                self.ultimo_id = self.get_ultimo_id()
                return True
            else:
                Logger.add_to_log("error", str('El usuario ya existe'))
                return False
        except Exception as err:
            print(err)
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())

    def get_usuarios(self):

        query = '''
                SELECT us.id_usuario, us.usuario, us.password, us.f_registro, 
                us.f_modificacion, us.id_rol, rol.nombre_rol, us.id_empresa, em.nombre_empresa, us.estado
                FROM usuarios as us 
                inner join empresas as em 
                on us.id_empresa = em.id_empresa  
                inner join roles as rol 
                on us.id_rol = rol.id_rol
                WHERE us.estado = %s
                order by us.id_usuario desc'''

        params = ('0')
        return self.execute_query(query, params=params, fetchall=True)

    def get_usuario(self, id_usuario):

        query = '''
            SELECT * FROM usuarios WHERE id_usuario = %s
            AND estado = %s'''
        params = (id_usuario, '0')
        return self.execute_query(query, params=params), self.id_rol

    def existe_usuario(self, _usuario):
        query = '''
            SELECT * FROM usuarios WHERE usuario = %s 
            AND estado = %s '''
        params = (_usuario, '0')
        return self.execute_query(query, params=params)

    def validar_usuario(self, _usuario, id_empresa, password):
        self.id  = id_empresa
        query = '''
            SELECT us.id_usuario, us.usuario, us.password, us.id_rol from usuarios as us
            INNER JOIN empresas as em
            ON em.id_empresa = us.id_empresa  
            WHERE us.usuario = %s
            AND us.estado = %s AND em.estado = %s 
            AND us.id_empresa = %s'''
        params = (_usuario, '0', '0', id_empresa)
        row = self.execute_query(query, params=params)
        if row != None:
            self.id_rol = row['id_rol']
            user = User(row['id_usuario'], row['usuario'],
                        User.check_password(row['password'], password))
            return user, row['id_rol']
        else:
            return None, None

    def get_ultimo_id(self):
        query = '''
            SELECT id_usuario FROM usuarios ORDER BY id_usuario DESC LIMIT 1'''
        return self.execute_query(query)['id_usuario']

    def get_by_id(self, id):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT id_usuario, usuario FROM usuarios WHERE id_usuario = {}".format(
                id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row['id_usuario'], row['usuario'], None)
            else:
                return None
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())

    def update_usuario(self, usuario, password, id_rol, id_empresa, id_usuario):
        try:
            if len(password) < 100:
                password_hash = generate_password_hash(password)
            else:
                password_hash = password
            with mysql.connection.cursor() as cursor:
                cursor.execute('''
                                UPDATE usuarios 
                                SET usuario = %s, password = %s, f_modificacion = %s, 
                                id_rol = %s, id_empresa = %s
                                WHERE id_usuario = %s ''',
                               (usuario, password_hash, self.getFecha(), id_rol, id_empresa, id_usuario))
            mysql.connection.commit()
            return True
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    def delete_usuario(self, id_usuario, estado):
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute('''
                                UPDATE usuarios 
                                SET estado = %s, f_modificacion = %s
                                WHERE id_usuario = %s''',
                               (estado, self.getFecha(), id_usuario))
            mysql.connection.commit()
            return True
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    def get_usuarios_empresas(self):
        query = '''
            SELECT us.id_usuario, us.usuario, us.password, us.f_registro, 
                us.f_modificacion, us.id_rol, rol.nombre_rol, us.id_empresa, em.nombre_empresa, us.estado
                FROM usuarios as us 
                inner join empresas as em 
                on us.id_empresa = em.id_empresa  
                inner join roles as rol 
                on us.id_rol = rol.id_rol
                WHERE us.estado = %s and em.id_empresa = %s and rol.id_rol = %s
                order by us.id_usuario desc'''
        params = ('0', self.id, '3')
        return self.execute_query(query, params=params, fetchall=True)
    
    def get_nombre_empresa(self):
        query = '''
            SELECT us.id_rol, rol.nombre_rol, us.id_empresa, em.nombre_empresa 
                FROM usuarios as us 
                inner join empresas as em 
                on us.id_empresa = em.id_empresa  
                inner join roles as rol 
                on us.id_rol = rol.id_rol
                WHERE us.estado = %s and rol.id_rol = %s and em.id_empresa = %s
                order by us.id_usuario desc LIMIT 1
                '''
        params = ('0', self.id_rol, self.id)
        return self.execute_query(query, params=params)
    
    def get_empleados_empresa(self):
        query = '''
        select em.id_empleado, em.nombre, em.apellido, em.dpi, em.nit, em.igss, 
        em.direccion, em.telefono, em.correo, em.genero, emp.nombre_empresa, p.puesto, em.estado
        from empleados as em
        inner join puestos as p
        on em.id_puesto = p.id
        inner join empresas as emp
        on emp.id_empresa = em.id_empresa 
        where em.estado = %s AND emp.id_empresa = %s order by id_empleado desc'''
        params = ('0',self.id)
        return self.execute_query(query, params=params, fetchall=True)
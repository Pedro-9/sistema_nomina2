from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, password, id_role) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.id_role = id_role

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)


class Usuario:
    def __init__(self):
        self.id = 0
        self.id_role = 0
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

    def insert_usuario(self, usuario, password, id_role, id_empresa):
        try:
            password_hash = generate_password_hash(password)
            if self.existe_usuario(usuario) == None:
                with mysql.connection.cursor() as cursor:
                    cursor.execute('''
                                INSERT INTO usuarios(
                                usuario, password, f_registro,
                                f_modificacion, estado, id_rol, id_empresa) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                   (usuario, password_hash, self.getFecha(), self.getFecha(), '0', id_role, id_empresa))
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
        return self.execute_query(query, params=params), self.id_role

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
            self.id_role = row['id_rol']
            user = User(row['id_usuario'], row['usuario'],
                        User.check_password(row['password'], password), None)
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
            sql = "SELECT id_usuario, usuario, id_rol FROM usuarios WHERE id_usuario = {}".format(
                id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row['id_usuario'], row['usuario'], None, row['id_rol'])
            else:
                return None
        except Exception as err:
            Logger.add_to_log("error", str(err))
            Logger.add_to_log("error", traceback.format_exc())

    def update_usuario(self, usuario, password, id_role, id_empresa, id_usuario):
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
                               (usuario, password_hash, self.getFecha(), id_role, id_empresa, id_usuario))
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
        params = ('0', self.id_role, self.id)
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
    

    def get_nomina_data(self):
        query = '''
            SELECT
			e.id_empleado,
            CONCAT(e.nombre, ' ', e.apellido) as nombre,
            r.nombre_rol,
            n.dias,
            pues.sueldo,
            n.horas_extra,
            f_valorHora(pues.sueldo, n.horas_extra) as valor,
            n.comisiones,
            n.bonificaciones,
            (pues.sueldo + f_valorHora( pues.sueldo, n.horas_extra) + n.comisiones) AS TOTAL_DEVENGADO,
            f_igss(pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss) AS IGGS,
            f_ISR(pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) AS ISR,
            an.monto as anticipo,
            p.monto as descuento_prestamo,
            (f_igss( pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss) + 
             f_ISR( pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) + 
             an.monto + p.monto) AS TotalDescuento,
            (( pues.sueldo + f_valorHora( pues.sueldo, n.horas_extra) + n.comisiones) - 
             (f_igss( pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss) + 
              f_ISR( pues.sueldo, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) + 
              an.monto + p.monto)) AS TOTAL_LIQUIDO
            FROM empleados e
            INNER JOIN usuarios u ON e.id_usuario = u.id_usuario
            INNER JOIN roles r ON u.id_rol = r.id_rol
            INNER JOIN nominas n ON e.id_empleado = n.id_empleado
            INNER JOIN bauchers b ON n.id_nomina = b.id_nomina
            INNER JOIN PRESTAMOS p ON u.id_usuario = p.id_usuario_solicita
            INNER JOIN anticipos an ON u.id_usuario = an.id_usuario
            INNER JOIN puestos pues ON e.id_empleado = pues.id
            WHERE e.id_empresa = %s ;
        '''
        params = (self.id)
        return self.execute_query(query, params = params, fetchall=True)
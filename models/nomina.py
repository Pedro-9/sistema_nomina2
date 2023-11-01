from db import mysql
from datetime import datetime
import traceback
from utils.Logger import Logger

class Nomina:
    def __init__(self):
        self.usuario = ""
        self.nombre = ""
        self.nombre_rol = ""
        self.salario_base = 0
        self.horas_extra = 0
        self.comisiones = 0
        self.bonificaciones = 0
        self.descuento_igss = 0
        self.descuento_isr = 0
        self.anticipo = 0
        self.descuento_prestamo = 0

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
        return self.execute_query(query, fetchall=True)

    def get_single_nomina(self, id_nomina):
        query = '''
        SELECT
            u.usuario,
            CONCAT(nombre, ' ', apellido) as nombre,
            r.nombre_rol,
            e.salario_base,
            n.horas_extra,
            f_valorHora(e.salario_base, n.horas_extra) as valor,
            n.comisiones,
            n.bonificaciones,
            (e.salario_base + f_valorHora(e.salario_base, n.horas_extra) + n.comisiones) AS TOTAL_DEVENGADO,
            f_igss(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss) AS IGGS,
            f_ISR(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) AS ISR,
            b.anticipo,
            b.descuento_prestamo,
            (f_igss(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss) + 
             f_ISR(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) + 
             b.anticipo + b.descuento_prestamo) AS TotalDescuento,
            ((e.salario_base + f_valorHora(e.salario_base, n.horas_extra) + n.comisiones) - 
             (f_igss(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss) + 
              f_ISR(e.salario_base, n.horas_extra, n.comisiones, b.descuento_igss, b.descuento_isr, n.bonificaciones) + 
              b.anticipo + b.descuento_prestamo)) AS TOTAL_LIQUIDO
        FROM empleados e
        INNER JOIN usuarios u ON e.id_usuario = u.id_usuario
        INNER JOIN roles r ON u.id_rol = r.id_rol
        INNER JOIN nominas n ON e.id_empleado = n.id_empleado
        INNER JOIN bauchers b ON n.id_nomina = b.id_nomina
        WHERE n.id_nomina = %s;
        '''
        return self.execute_query(query, params=(id_nomina,))





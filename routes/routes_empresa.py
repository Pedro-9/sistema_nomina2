from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.empresa import Empresa
from models.usuario import Usuario
from models.nomina import Nomina
from models.prestamo import Prestamo
from models.nominass import Nominass
from models.anticipos import Anticipo
from utils.Logger import Logger
from flask_login import login_required

# objeto del controlador usuario
empresa = Empresa()
user = Usuario()
nomina = Nomina()
nominass = Nominass()
prestamo = Prestamo()
anticipo = Anticipo()
empresas = Blueprint('empresas', __name__, template_folder='templates')


@empresas.route('/empresas')
@login_required
def getEmpresas():
    row = empresa.get_empresas()
    if row != None:
        return jsonify({"empresas": row})
    else:
        return jsonify({"mensaje": "No existe empresas"})

@empresas.route('/show_companies')
@login_required
def mostrar_empresas():
    return render_template('panel/empresas.html')

# Ruta para obtener una empresa
# ----------------------------
@empresas.route('/empresa/<string:id_empresa>')
@login_required
def getEmpresa(id_empresa):
    row = empresa.get_empresa(id_empresa)
    if row != None:
        return jsonify({"Empresa": row})
    else:
        return jsonify({"mensaje": "Empresa no existe"})

# Ruta para insetar nueva empresa
# -------------------------------
@empresas.route('/insert_empresa', methods=['POST'])
@login_required
def insertEmpresa():
    if request.method == 'POST':
        var_empresa = request.json['empresa']
        try:
            response = empresa.insert_empresa(var_empresa)
            
            if response:
                Logger.add_to_log(
                    "info", f"Empresa agregado exitosamente -->{var_empresa}")
                return jsonify({"mensaje": "Empresa agregado exitosamente"})
            else:
                Logger.add_to_log("info", "Empresa ya existe")
                return jsonify({"mensaje": "Empresa ya existe"})
        except Exception as e:
            return redirect(url_for('empresas.mostrar_empresas'))


@empresas.route('/update_empresa', methods=['POST'])
@login_required
def updateEmpresa():
    if request.method == 'POST':
        nombre_empresa = request.json['empresa']
        id_empresa = request.json['id']

        try:
            response = empresa.update_empresa(nombre_empresa, id_empresa)
            if response:
                Logger.add_to_log("info", f"Empresa actualializado exitosamente id: {id_empresa} nombre: {nombre_empresa}")
                return jsonify({"mensaje": "Empresa actualizado exitosamente"})
            else:
                Logger.add_to_log("info", f"Error al actualizar empresa id:{id_empresa} nombre: {nombre_empresa}")
                return jsonify({"mensaje": "Error al actualizar registro"})
        except Exception as err:
            Logger.add_to_log('error', err)
            return redirect(url_for('empresas.mostrar_empresas'))


@empresas.route('/delete_empresa/<string:id>', methods=['POST', 'GET'])
@login_required
def deleteEmpresa(id):
    try:
        response = empresa.delete_empresa(id,'1')
        if response:
            Logger.add_to_log("info", f"Empresa eliminado exitosamente id: {id}")
            return jsonify({"mensaje": "Emprea eliminado exitosamente"})
        else:
            Logger.add_to_log("info", "Error al elimianr registro")
            return jsonify({"mensaje": "Error al eliminar registro"})
    except Exception as err:
        Logger.add_to_log('error', err)
        return redirect(url_for('empresas.mostrar_empresas'))
    
@empresas.route('/show_user_companie')
@login_required
def mostrar_usuarios_empresa():
    return render_template('panel/usuario_empresa.html')


# Ruta para nomina
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



# @empresas.route('/nominas')
# @login_required
# def getNominas():
#     nominas_data = user.get_nomina_data()
#     if nominas_data is not None:
#         return jsonify({"nominas": nominas_data})
#     else:
#         return jsonify({"mensaje": "No existen nóminas"})


@empresas.route('/show_user_nomina')
@login_required
def mostrar_nomina():
    return render_template('panel/nomina.html')

# Ruta para Prestamo
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


@empresas.route('/prestamos')
@login_required
def getPrestamos():
    prestamos = prestamo.get_prestamos()
    if prestamos !=None:
        return jsonify({"prestamos": prestamos})
    else:
        return jsonify({"mensaje": "No existe roles"})
    
@empresas.route('/show_user_prestamos')
@login_required
def mostrar_prestamos():
    return render_template('panel/prestamos.html')


@empresas.route('/insert_prestamo', methods=['POST'])
@login_required
def insertPrestamo():
    if request.method == 'POST':
        fecha_atencion = request.json['fecha_atencion']
        descripcion = request.json['descripcion']
        plazo_meses = request.json['plazo_meses']
        monto = request.json['monto']
        estado = request.json['estado']
        id_usuario_solicita = request.json['id_usuario_solicita']
        id_usuario_atiende = request.json['id_usuario_atiende']

        try:
            response = prestamo.insert_prestamo(
                fecha_atencion, descripcion, plazo_meses, monto, estado, id_usuario_solicita, id_usuario_atiende)
            if response:
                Logger.add_to_log("info", "Préstamo agregado exitosamente")
                return jsonify({"mensaje": "Préstamo agregado exitosamente"})
        except Exception as e:
            return jsonify({"mensaje": "Error al agregar préstamo"})

# Ruta para Anticipo
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@empresas.route('/anticipos')
@login_required
def getAnticipos():
    anticipos = anticipo.get_anticipos()
    if anticipos is not None:
        return jsonify({"anticipos": anticipos})
    else:
        return jsonify({"mensaje": "No existen anticipos"})


    
@empresas.route('/show_user_anticipos')
@login_required
def mostrar_anticipo():
    return render_template('panel/anticipo.html')


@empresas.route('/insert_anticipo', methods=['POST'])
@login_required
def insertAnticipo():
    if request.method == 'POST':
        fecha_atencion = request.json['fecha_atencion']
        fecha_pago = request.json['fecha_pago']
        descripcion = request.json['descripcion']
        monto = request.json['monto']
        estado = request.json['estado']
        id_usuario = request.json['id_usuario']

        try:
            response = anticipo.insert_anticipo(
                fecha_atencion, fecha_pago, descripcion, monto, estado, id_usuario)
            if response:
                Logger.add_to_log("info", "Anticipo agregado exitosamente")
                return jsonify({"mensaje": "Anticipo agregado exitosamente"})
        except Exception as e:
            return jsonify({"mensaje": "Error al agregar anticipo"})
        



# Ruta para Nominas
# - - - - - - - - - - - - - - 

@empresas.route('/nominass')
@login_required
def getNominass():
    nominas = nominass.get_nominas()
    if nominas is not None:
        return jsonify({"nominas": nominas})
    else:
        return jsonify({"mensaje": "No existen nóminas"})

@empresas.route('/show_user_nominass')
@login_required
def mostrar_nominass():
    return render_template('panel/nominas.html')

@empresas.route('/insert_nomina', methods=['POST'])
@login_required
def insertNomina():
    if request.method == 'POST':
        id_empleado = request.json['id_empleado']
        fecha = request.json['fecha']
        horas_trabajadas = request.json['horas_trabajadas']
        ausencia_dias = request.json['ausencia_dias']
        horas_extra = request.json['horas_extra']
        comisiones = request.json['comisiones']
        bonificacion = request.json['bonificacion']
        estado = request.json['estado']

        try:
            response = nominass.insert_nomina(
                id_empleado, fecha, horas_trabajadas, ausencia_dias, horas_extra, comisiones, bonificacion, estado)
            if response:
                Logger.add_to_log("info", "Nómina agregada exitosamente")
                return jsonify({"mensaje": "Nómina agregada exitosamente"})
        except Exception as e:
            return jsonify({"mensaje": "Error al agregar nómina"})
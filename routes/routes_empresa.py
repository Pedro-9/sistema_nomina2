from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.empresa import Empresa
from models.usuario import Usuario
from utils.Logger import Logger
from flask_login import login_required

# objeto del controlador usuario
empresa = Empresa()
user = Usuario()
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
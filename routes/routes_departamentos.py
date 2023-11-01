from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.departamentos import Departamento
from utils.Logger import Logger
from flask_login import login_required

# objeto del controlador departamento
departamento = Departamento()

departamentos = Blueprint('departamento', __name__, template_folder='templates')

@departamentos.route('/departamentos')
def getDepartamentos():
    departamentos = departamento.get_departamentos()
    if departamentos !=None:
        return jsonify({"departamentos": departamentos})
    else:
        return jsonify({"mensaje": "No existen departamentos"})
    
@departamentos.route('/show_departments')
@login_required
def mostrar_departamentos():
    return render_template('panel/departamentos.html')
    
# Ruta para obtener una departamento
# ----------------------------
@departamentos.route('/departamento/<string:id_departamento>')
@login_required
def getDepartamento(id_departamento):
    row = departamento.get_departamento(id_departamento)
    if row!=None:
        return jsonify({"Departamento": row})
    else:
        return jsonify({"mensaje": "No existe Departamento"})
    

@departamentos.route('/insert_departamento', methods=['POST'])
@login_required
def insertDepartamento():
    if request.method == 'POST':
        var_departamento = request.json['departamento']
        var_usuario = request.json['usuario']
        try:
            response = departamento.insert_departamento(var_departamento, var_usuario)
            print(response)
            if response:
                Logger.add_to_log(
                    "info", f"Departamento agregado exitosamente -->{var_departamento}")
                return jsonify({"mensaje": "Departamento agregado exitosamente"})
            elif response == None:
                Logger.add_to_log("info", "Departamento ya existe")
                return jsonify({"mensaje": "Departamento ya existe"})
        except Exception as e:
            return redirect(url_for('departamentos.mostrar_departamentos'))


@departamentos.route('/update_departamento', methods=['POST'])
@login_required
def updateDepartamento():
    if request.method == 'POST':
        nombre_departamento = request.json['departamento']
        id_usuario = request.json['usuario']
        id_departamento = request.json['id']

        try:
            response = departamento.update_departamento(nombre_departamento, id_usuario, id_departamento)
            if response:
                Logger.add_to_log("info", f"Departamentool actualializado exitosamente id: {id_departamento} nombre: {nombre_departamento}")
                return jsonify({"mensaje": "Departamento actualizado exitosamente"})
            else:
                Logger.add_to_log("info", f"Error al actualizar departamento id:{id_departamento} nombre: {nombre_departamento} usuario: {id_usuario}")
                return jsonify({"mensaje": "Error al actualizar registro"})
        except Exception as err:
            Logger.add_to_log('error', err)
            return redirect(url_for('departamentos.mostrar_departamentos'))


@departamentos.route('/delete_departamento/<string:id>', methods=['POST', 'GET'])
@login_required
def deleteDepartamento(id):
    try:
        response = departamento.delete_departamento(id,'1')
        if response:
            Logger.add_to_log("info", f"Departamento eliminado exitosamente id: {id}")
            return jsonify({"mensaje": "Departamento eliminado exitosamente"})
        else:
            Logger.add_to_log("info", "Error al elimianr registro")
            return jsonify({"mensaje": "Error al eliminar registro"})
    except Exception as err:
        Logger.add_to_log('error', err)
        return redirect(url_for('departamentos.mostrar_departamentos'))

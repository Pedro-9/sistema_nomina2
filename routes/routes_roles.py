from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.roles import Rol
from utils.Logger import Logger
from flask_login import login_required

# objeto del controlador rol
rol = Rol()

roles = Blueprint('roles', __name__, template_folder='templates')

@roles.route('/roles')
def getRoles():
    roles = rol.get_roles()
    if roles !=None:
        return jsonify({"roles": roles})
    else:
        return jsonify({"mensaje": "No existe roles"})
    
@roles.route('/show_roles')
@login_required
def mostrar_roles():
    return render_template('panel/rol.html')
    
# Ruta para obtener una rol
# ----------------------------
@roles.route('/rol/<string:id_rol>')
@login_required
def getRol(id_rol):
    row = rol.get_rol(id_rol)
    if row!=None:
        return jsonify({"Rol": row})
    else:
        return jsonify({"mensaje": "No existe rol"})
    

@roles.route('/insert_rol', methods=['POST'])
@login_required
def insertRol():
    if request.method == 'POST':
        var_rol = request.json['rol']
        try:
            response = rol.insert_rol(var_rol)
            print(response)
            if response:
                Logger.add_to_log(
                    "info", f"Rol agregado exitosamente -->{var_rol}")
                return jsonify({"mensaje": "Rol agregado exitosamente"})
            elif response == None:
                Logger.add_to_log("info", "Rol ya existe")
                return jsonify({"mensaje": "Rol ya existe"})
        except Exception as e:
            return redirect(url_for('roles.mostrar_roles'))


@roles.route('/update_rol', methods=['POST'])
@login_required
def updateRol():
    if request.method == 'POST':
        nombre_rol = request.json['rol']
        id_rol = request.json['id']

        try:
            response = rol.update_rol(nombre_rol, id_rol)
            if response:
                Logger.add_to_log("info", f"Rol actualializado exitosamente id: {id_rol} nombre: {nombre_rol}")
                return jsonify({"mensaje": "Rol actualizado exitosamente"})
            else:
                Logger.add_to_log("info", f"Error al actualizar rol id:{id_rol} nombre: {nombre_rol}")
                return jsonify({"mensaje": "Error al actualizar registro"})
        except Exception as err:
            Logger.add_to_log('error', err)
            return redirect(url_for('roles.mostrar_roles'))


@roles.route('/delete_rol/<string:id>', methods=['POST', 'GET'])
@login_required
def deleteRol(id):
    try:
        response = rol.delete_rol(id,'1')
        if response:
            Logger.add_to_log("info", f"Rol eliminado exitosamente id: {id}")
            return jsonify({"mensaje": "Rol eliminado exitosamente"})
        else:
            Logger.add_to_log("info", "Error al elimianr registro")
            return jsonify({"mensaje": "Error al eliminar registro"})
    except Exception as err:
        Logger.add_to_log('error', err)
        return redirect(url_for('roles.mostrar_roles'))

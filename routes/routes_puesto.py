from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from models.puesto import Puesto
from flask_login import login_required

# objeto del controlador rol
puesto = Puesto()

puestos = Blueprint('puestos', __name__, template_folder='templates')

@login_required
@puestos.route('/puestos')
def getRoles():
    row = puesto.get_puestos()
    if row !=None:
        return jsonify({"puestos": row})
    else:
        return jsonify({"mensaje": "No existe puestos"})
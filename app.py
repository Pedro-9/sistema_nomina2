from my_app import app
from flask import redirect, url_for
from flask_login import LoginManager
from models.usuario import Usuario
from routes.routes_usuario import usuario
from routes.routes_roles import roles
from routes.routes_empresa import empresas
from routes.routes_empleado import empleados
from routes.routes_puesto import puestos


login_manager_app = LoginManager(app)

user = Usuario()

@login_manager_app.user_loader
def load_user(id):
    return user.get_by_id(id)

app.register_blueprint(usuario)
app.register_blueprint(roles)
app.register_blueprint(empresas)
app.register_blueprint(empleados)
app.register_blueprint(puestos)


def status_401(error):
    return redirect(url_for('usuario.index_login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=3000, debug=True)
    
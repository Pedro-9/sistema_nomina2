from flask import Flask

# Inicializar aplicacion
app = Flask(__name__)
# Configuracion
app.secret_key = "mysecretkey"


import os
from flask import Flask

# INICIALIZACION DE LA CLASE APP
app = Flask("Main")

# VARIABLES

# FUNCIONES

# PAGINAS ESTATICAS
@app.route("/")
def index():
  return "WIP"

# PAGINAS DINAMICAS

# INICIO DEL SERVIDOR
app.run("0.0.0.0",8080)
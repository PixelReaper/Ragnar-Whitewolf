# IMPORTACION DE LIBRERIAS:
from flask import Flask, render_template, send_file
from random import randint as random
from flask_misaka import Misaka
import shutil
import os

# CREACION DE LA CLASE APP:
app = Flask(__name__)
Misaka(app)

# VARIABLES DE CONFIGURACION:
BLOG_VERSION = "2.0.0"

IP = "0.0.0.0"
PUERTO = 8080

POSTS   = os.getcwd()+"/Publicaciones/"
PAGINAS = os.getcwd()+"/Paginas/"
ERRORES = PAGINAS + "Errores/"
# OTRAS VARIABLES:
TEP = "En construccion."

# FUNCIONES:
def mdread(ifile): # LECTOR DE MARKDOWN
  ifile = open(ifile,"r")
  result = ifile.read()
  ifile.close()
  ifile = None
  return result

def docread(key): # LECTOR DE DOCUMENTOS EN FORMATO DE CLAVE
  key = open(key+"/document.md","r")
  result = key.read()
  key.close()
  key = None
  return result

def getfragment(key): # LECTOR DE FRAGMENTO DE CLAVE
  key = open(key+"/fragment.md","r")
  result = key.read()
  key.close()
  key = None
  return result

def readmeta(key): # LECTOR DE PROPIEDADES DE CLAVE
  ktitle = ""
  kdate  = ""
  kimage = ""
  key = open(key+"/meta.prop","r")
  undata = key.read().split("\n")
  key.close()

  for i in range(0,len(undata)):
    if "$Date" in undata[i]:
      kdate = undata[i].replace("$Date = ","")
      kdate = kdate.split(" ")
    elif "$Title" in undata[i]:
      ktitle = undata[i].replace("$Title = ","")
    elif "$Image" in undata[i]:
      kimage = undata[i].replace("$Image = ","")
  undata = None
  result = [kdate,ktitle,kimage]
  kdate  = None
  ktitle = None
  kimage = None
  key = None

  return result

def generateHome(): # GENERADOR DE PAGINA DE INICIO
  print(" * Generando pagina de inicio")
  PList      = mdread(POSTS+"Indice").split("\n")
  Pdates     = {}
  Ptitles    = {}
  Pimages    = {}
  Pfragments = {}
  Pbox       = {}
  document   = ""
  # LEER Y GUARDAR METADATOS:
  for rk in range(0,len(PList)):
    temp = readmeta(POSTS+PList[rk])
    Pdates[rk] = temp[0]
    Ptitles[rk] = temp[1]
    Pimages[rk] = temp[2]
    temp = getfragment(POSTS+PList[rk])
    Pfragments[rk] = temp
    temp = None
  # GENERAR DOCUMENTO:
  for pb in range(0,len(PList)):
    Pbox[pb] = "<h1>"+Ptitles[pb]+"</h1><p>[ "+Pdates[pb][0]+"/"+Pdates[pb][1]+"/"+Pdates[pb][2]+" ]</p><br><img src=\""+"/static/img/post/"+Pimages[pb]+"\"><br>"+Pfragments[pb]+"<br><br><a href=\"/entrada/"+PList[pb]+"\">Seguir Leyendo</a><br><hr>"
  for dr in range(0,len(Pbox)):
    document = document + Pbox[dr] + "\n\n"
  # ESCRIBIR DOCUMENTO:
  ifile = open(PAGINAS+"Inicio.md","w")
  ifile.write(document)
  ifile.close()
  # LIMPIEZA DE VARIABLES:
  ifile      = None
  PList      = None
  Pdates     = None
  Ptitles    = None
  Pimages    = None
  Pfragments = None
  Pbox       = None
  document   = None
  print(" * Pagina de inicio generada")

def getSource(): # COMPRIME Y DEVUELVE UNA CADENA DE TEXTO CON LA RUTA ABSOLUTA DEL ARCHIVO
  nam = str(random(100000,999999))
  os.system("mkdir /tmp/"+nam)
  os.system("cp -r /home/runner/Paginas /tmp/"+nam)
  os.system("cp -r /home/runner/Publicaciones /tmp/"+nam)
  os.system("cp -r /home/runner/static /tmp/"+nam)
  os.system("cp -r /home/runner/templates /tmp/"+nam)
  os.system("cp -r /home/runner/LICENSE.md /tmp/"+nam)
  os.system("cp -r /home/runner/requirements.txt /tmp/"+nam)
  os.system("cp -r /home/runner/main.py /tmp/"+nam)
  shutil.make_archive("/tmp/"+nam,"zip","/tmp/"+nam+"/")
  os.system("rm -rf /tmp/"+nam+"/")
  return "/tmp/"+nam+".zip"

# PAGINAS ESTATICAS:
@app.route("/")
def index():
    homepage = mdread(PAGINAS + "Inicio.md")
    return render_template("page.html", content=homepage, title="Pixel Reaper")

@app.route("/keybase.txt")
def keybase():
  keybase_text = mdread(PAGINAS + "Keybase.txt")
  return keybase_text

@app.route("/proyectos")
def projects():
    projectspage = ""
    with open(PAGINAS + "Proyectos.md", "r") as f:
        projectspage = f.read()

    return render_template(
        "page.html", content=projectspage, title="Pixel Reaper | Mis proyectos")


@app.route("/codigo-fuente")
def source():
    sourcepage = ""
    with open(PAGINAS + "Codigo.md", "r") as f:
        sourcepage = f.read()

    return render_template(
        "page.html", content=sourcepage, title="Pixel Reaper | Codigo Fuente")


@app.route("/sobre-mi")
def about():
    aboutpage = ""
    with open(PAGINAS + "Sobre-mi.md", "r") as f:
        aboutpage = f.read()

    return render_template(
        "page.html", content=aboutpage, title="Pixel Reaper | Sobre Mi")

@app.route("/donar")
def donate():
  donatepage = ""
  with open(PAGINAS + "Donaciones.md", "r") as f:
    donatepage = f.read()
  
  return render_template("page.html", content=donatepage, title="Pixel Reaper | Donar")


# PAGNIAS DINAMICAS:
@app.route("/entrada/<name>")  # POSTS
def post(name):
  CONTENT = docread(POSTS+name)
  KEY = readmeta(POSTS+name)
  TITLE   = KEY[1]
  DATE    = KEY[0][0]+"/"+KEY[0][1]+"/"+KEY[0][2]
  IMAGE   = "/static/img/post/"+KEY[2]
  KEY = None
  return render_template("post.html",DATE=DATE, TITLE=TITLE, PTITLE=TITLE, IMAGE=IMAGE,CONTENT=CONTENT)

# PAGINAS DE ERROR
@app.errorhandler(401)
def error_401(pos):
    error401 = ""
    with open(ERRORES + "401.md", "r") as f:
        error401 = f.read()

    return render_template("page.html", title="ERROR!", content=error401)


@app.errorhandler(403)
def error_403(pos):
    error403 = ""
    with open(ERRORES + "403.md", "r") as f:
        error403 = f.read()

    return render_template("page.html", title="ERROR!", content=error403)


@app.errorhandler(404)
def error_404(pos):
    error404 = ""
    with open(ERRORES + "404.md", "r") as f:
        error404 = f.read()

    return render_template("page.html", title="ERROR!", content=error404)


@app.errorhandler(500)
def error_500(pos):
    error500 = ""
    with open(ERRORES + "500.md", "r") as f:
        error500 = f.read()

    return render_template("page.html", title="ERROR!", content=error500)


@app.errorhandler(503)
def error_503(pos):
    error503 = ""
    with open(ERRORES + "503.md", "r") as f:
        error503 = f.read()

    return render_template("page.html", title="ERROR!", content=error503)

# INICIO DEL SERVIDOR
generateHome()
app.run(host=IP, port=PUERTO)
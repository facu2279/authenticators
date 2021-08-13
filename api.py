"""****************************************************************
*******************************************************************
***  Made by Facundo Diaz - August 2021                         ***
***                                                             ***
***  Documentation about PyOTP Library                          ***
***  https://pyauth.github.io/pyotp/                            ***
***                                                             ***
***                                                             ***
*******************************************************************
****************************************************************"""
#Importo librerias necesarias

from datetime import datetime
from flask_mysqldb import MySQL
import pyotp
from flask import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'testing'
mysql = MySQL(app)
# diccionario de prueba para hacer testeos hasta agregar database

administradores = {}

# homepage route to check
@app.route("/")
def index():
    return "Online"

""" """
@app.route("/test/validar_pin", methods=["GET", "POST"])
def a():
    user = str(request.args.get('user'))
    pin = str(request.args.get('pin'))
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT secret_key FROM usuarios_qr WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    if resultado:
        secret_key_user = str(resultado[0][0])
        if pin:
            if (secret_key_user):
                totp = pyotp.TOTP(secret_key_user)
                return str(totp.verify(pin))
            else:
                return "Error"
        else:
            return "Ingrese un pin a validar"
    else:
        return "Usuario no valido"

""" """
@app.route("/test/generar_usuario", methods=["GET", "POST"])
def b():
    dict_to_bdd = {}
    user = str(request.args.get('user'))
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT * FROM usuarios_qr WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    if resultado:
        return user +  " ya tiene un qr activo"
    else:
        secret_key = pyotp.random_base32()
        qr = str(pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="App_Testing"))
        dict_to_bdd['user'] = user
        dict_to_bdd['secret_key'] = str(secret_key)
        dict_to_bdd['qr'] = qr
        fecha = datetime.now()
        fecha = fecha.strftime("%Y-%m-%d")
        dict_to_bdd['fecha'] = fecha
        guardar_usuario(dict_to_bdd)
        return str(qr)

""" """
@app.route("/test/login", methods=["GET", "POST"])
def c():
    user = str(request.args.get('user'))
    password = str(request.args.get('password'))

    if user != "" and user != None and password != "" and password != None:
        consulta = mysql.connection.cursor()
        consulta.execute("SELECT * FROM usuarios;")
        resultado = consulta.fetchall()
        for i in resultado:
            administradores[i[1]] = i[2]
        if user in administradores:
            if password == administradores[user]:
                return "True"
    
    return "False"

""" DATABASE SECTION """
def guardar_usuario(dict):
    sql = "INSERT INTO usuarios_qr (usuario, secret_key, qr, fecha) VALUES ('" + dict['user'] + "', '" + dict['secret_key'] + "', '" + dict['qr'] + "', '" + dict['fecha'] + "');"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

# running flask server
if __name__ == "__main__":
    # para correr en localhost usar este
    app.run(host='0.0.0.0')
    # para correr en servidor usar este
    #app.run(host='0.0.0.0, port=8080)
    
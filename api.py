"""**********************************************************************
*************************************************************************
***  Made by Facundo Diaz - August 2021                               ***
***                                                                   ***
*** END-POINTS: 1- /test/validar_pin                                  ***
***             2- /test/generar_usuario                              ***
***             3- /test/login                                        ***
***             4- /test                                              ***
***                                                                   ***
***                                                                   ***
***                                                                   ***
***  PyOTP Library Documentation                                      ***
***  https://pyauth.github.io/pyotp/                                  ***
***                                                                   ***
***                                                                   ***
***  Flask’s documentation                                            ***
***  https://flask.palletsprojects.com/en/2.0.x/                      ***
***                                                                   ***
***                                                                   ***
***  Flask-MySQLdb’s documentation                                    ***
***  https://docs.python.org/3/library/datetime.html                  ***
***                                                                   ***
***                                                                   ***
***  Flask-CORS                                                       ***
***  https://flask-cors.readthedocs.io/en/latest/                     ***
***                                                                   ***
***                                                                   ***
***  datetime — Basic date and time types                             ***
***  https://docs.python.org/3/library/datetime.html                  ***
***                                                                   ***
*************************************************************************
**********************************************************************"""
#Importo librerias necesarias

from datetime import datetime
from flask_mysqldb import MySQL
import pyotp
from flask import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


"""***********************************

SET VARIABLES TO CONNECT WITH DATABASE

***********************************"""

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'testing'
mysql = MySQL(app)


"""*****************************

HOME - CHECK IF SERVER IS ONLINE

*****************************"""
@app.route("/test")
def index():
    return "Online"



"""***********************

VALIDATE PIN

***********************"""
@app.route("/test/validar_pin", methods=["GET", "POST"])
def a():
    # user = request.form['user']
    # pin = request.form['pin']
    user = str(request.args.get('user'))
    pin = str(request.args.get('pin'))
    if user != "" and user != None:
        secret_key_user = traer_secret_key(user)
        if secret_key_user != "" and secret_key_user != None:
            if pin != "" and pin != None:
                if (secret_key_user):
                    totp = pyotp.TOTP(secret_key_user)
                    return str(totp.verify(pin))
                else:
                    return "Error"
            else:
                return "Error"
        else:
            return "Error"
    else:
        return "Error"


"""***********************

GENERATE A NEW USER

***********************"""
@app.route("/test/generar_usuario", methods=["GET", "POST"])
def b():
    usuario_a_guardar = {}
    # user = request.form['usuario']
    user = str(request.args.get('user'))
    if user != "" and user != None:
        resultado = chequear_existente(user)
        if resultado:
            return user +  " ya tiene un qr activo"
        else:
            secret_key = pyotp.random_base32()
            qr = str(pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="App_Testing"))
            usuario_a_guardar['user'] = user
            usuario_a_guardar['secret_key'] = str(secret_key)
            usuario_a_guardar['qr'] = qr
            fecha = datetime.now()
            fecha = fecha.strftime("%Y-%m-%d")
            usuario_a_guardar['fecha'] = fecha
            guardar_usuario(usuario_a_guardar)
            return str(qr)
    else:
        return "Error"

"""***********************

LOGIN

***********************"""

@app.route("/test/login", methods=["GET", "POST"])
def c():
    # user = request.form['usuario']
    # password = request.form['password']
    user = str(request.args.get('user'))
    password = str(request.args.get('password'))
    if user != "" and user != None and password != "" and password != None:
        pass_bdd = traer_password(user)
        if password == pass_bdd:
            return "True"
    return "False"


"""********************************

DATABASE SECTION

*************************************"""


"""

"""
def traer_secret_key(user):
    resultado = ""
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT secret_key FROM usuarios_qr WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    if resultado:
        resultado = str(resultado[0][0])
    return resultado

"""

"""
def guardar_usuario(dict):
    sql = "INSERT INTO usuarios_qr (usuario, secret_key, qr, fecha) VALUES ('" + dict['user'] + "', '" + dict['secret_key'] + "', '" + dict['qr'] + "', '" + dict['fecha'] + "');"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

"""

"""
def traer_password(user):
    resultado = ""
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT password FROM usuarios WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    if resultado:
        resultado = resultado[0][0]
        resultado = des(resultado)
    return str(resultado)

"""

"""
def chequear_existente(user):
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT * FROM usuarios_qr WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    return resultado

"""

"""
def enc(s):
    chars = "qwertyuioplkjhgfdsazxcvbnm"
    trans = chars[10:]+chars[:10]
    caracter = lambda c: trans[chars.find(c)] if chars.find(c)>-1 else c
    return ''.join( caracter(c) for c in s ) 
"""

"""
def des(s):
    for i in range(0,12):
        s = enc(s)
    return s


"""****************************

RUNNING FLASK SERVICES

*****************************"""
if __name__ == "__main__":
    # para correr en localhost usar este
    app.run(host='0.0.0.0')
    # para correr en servidor usar este
    #app.run(host='0.0.0.0, port=8080)
    
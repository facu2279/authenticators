"""**********************************************************************
*************************************************************************
***  Made by Facundo Diaz - August 2021                               ***
***                                                                   ***
*** END-POINTS: 1- /test/validar_pin                                  ***
***             2- /test/generar_usuario                              ***
***             3- /test/modificar_usuario                            ***
***             6- /test                                              ***
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
***  PyJWT Documentation                                              ***
***  https://pyjwt.readthedocs.io/en/latest/                          ***
***                                                                   ***
***                                                                   ***
***  datetime — Basic date and time types                             ***
***  https://docs.python.org/3/library/datetime.html                  ***
***                                                                   ***
*************************************************************************
**********************************************************************"""


# IMPORT LIBRARIES

from datetime import datetime
import string
import random
import pyotp
from flask_mysqldb import MySQL
from flask import *
from flask_cors import CORS
import jwt
import re
from werkzeug.datastructures import ContentSecurityPolicy
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



"""***************************************************************************

VALIDATE PIN
-------------------------
This end point receives the user and the pin by parameter, 
checks that they are not empty or null, then we bring the secret
key corresponding to that user from the database,
then we generate the totp object with that secret key and verify the pin
that the user passed us at that moment against the
one that has our object at this moment, 
if they coincide, return True, otherwise, return False, 
if any of the data to check is missing or invalid return Error

******************************************************************************"""
@app.route("/test/validar_pin", methods=["GET", "POST"])
def a():
    # If the data is passed to me through parameters inside the data section in the request, use this lines
    #user = request.form['user']
    #pin = request.form['pin']
    # If the data is passed to me by url, use this lines
    user = str(request.args.get('user'))
    pin = str(request.args.get('pin'))

    if user != "" and user != None and user != "None":
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


"""****************************************************************************

GENERATE A NEW QR
---------------------
This endpoint receives the user for whom we want to generate a qr,
we check that it is not empty or null,
then we check that that user does not have an active qr,
if it exists in our system we return that it already has a qr in use,
otherwise we generate it one. We generate a random secret key in base32
then we generate the prompt url for the qr,
we save the necessary data, user, secret key, qr, and the current date,
then we save it in the database and return the generated qr for the user scan

********************************************************************************"""
@app.route("/test/generar_usuario", methods=["GET", "POST"])
def b():
    usuario_a_guardar = {}
    # If the data is passed to me through parameters inside the data section in the request, use this line
    # user = request.form['usuario']
    # If the data is passed to me by url, use this line
    user = str(request.args.get('user'))
    if user != "" and user != None and user != "None":
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
    return "Error"


"""****************************************************************************

MODIFY QR
---------------------

This endpoint receives by parameter the username to which
we want to generate a new qr, we check that there is a user with that name,
we generate all the necessary data as in the / test / generate_user,
but the function that we call the database, it is an update and not an insert

********************************************************************************"""
@app.route("/test/modificar_usuario", methods=["GET", "POST"])
def e():
    usuario_a_guardar = {}
    # If the data is passed to me through parameters inside the data section in the request, use this line
    # user = request.form['usuario']
    # If the data is passed to me by url, use this line
    user = str(request.args.get('user'))
    if user != "" and user != None and user != "None":
        resultado = chequear_existente(user)
        if resultado:
            secret_key = pyotp.random_base32()
            qr = str(pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="App_Testing"))
            usuario_a_guardar['user'] = user
            usuario_a_guardar['secret_key'] = str(secret_key)
            usuario_a_guardar['qr'] = qr
            fecha = datetime.now()
            fecha = fecha.strftime("%Y-%m-%d")
            usuario_a_guardar['fecha'] = fecha
            modificar_qr(usuario_a_guardar)
            return str(qr)
    return "Error"


"""****************************************************************************

DELETE USER QR
---------------------

This endpoint receives the name of the user to delete, checks if it exists,
if it removes it from the database and returns Success,
if it does not exist, it returns Error

********************************************************************************"""
@app.route("/test/eliminar_usuario", methods=["GET", "POST"])
def f():
    # If the data is passed to me through parameters inside the data section in the request, use this line
    # user = request.form['usuario']
    # If the data is passed to me by url, use this line
    user = str(request.args.get('user'))
    if user != "" and user != None and user != "None":
        resultado = chequear_existente(user)
        if resultado:
            eliminar_user(user)
            return "Success"
    return "Error"


@app.route("/test/listar_usuarios", methods=["GET", "POST"])
def g():
    res = traer_usuarios()
    print(res)
    return res




"""********************************

DATABASE SECTION

*************************************"""


"""

This function searches the database for the secret key corresponding to the user

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

This function saves the generated qr with the user's data and date in the database

"""
def guardar_usuario(dict):
    sql = "INSERT INTO usuarios_qr (usuario, secret_key, qr, fecha) VALUES ('" + dict['user'] + "', '" + dict['secret_key'] + "', '" + dict['qr'] + "', '" + dict['fecha'] + "');"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

"""

This function checks if a user already has a generated qr in the database

"""
def chequear_existente(user):
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT * FROM usuarios_qr WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    return resultado

"""

This function updates the new qr data in the database

"""
def modificar_qr(usuario):
    sql = "UPDATE usuarios_qr SET qr='" + usuario['qr'] + "', fecha='" + usuario['fecha'] + "', secret_key='" + usuario['secret_key'] + "'"
    sql += "WHERE usuario='" + usuario['user'] + "'"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

"""

"""
def eliminar_user(user):
    sql = "DELETE FROM usuarios_qr WHERE usuario='" + user + "';"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

"""


"""
def traer_usuarios():
    usuarios = []
    usuario = {}
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT * FROM usuarios_qr;")
    resultado = consulta.fetchall()
    for i in resultado:
        usuario['id'] = i[0]
        usuario['usuario'] = i[1]
        usuario['secret_key'] = i[2]
        usuario['qr'] = i[3]
        date = i[4]
        usuario['date'] = date
        usuarios.append(usuario)
    
    string = ""
    for i in range(0, len(usuarios) - 1):
        string += str(usuarios[i])
        string += '\n'
    return string

"""

This function generates a random string of 10 characters

"""
def generar_key_random():
    length_of_string = 10
    return (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))

"""****************************

RUNNING FLASK SERVICES

*****************************"""
if __name__ == "__main__":
    # to run on localhost use this
    app.run(host='0.0.0.0')
    # to run on server, use this
    #app.run(host='0.0.0.0, port=8080)
    
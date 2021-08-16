"""**********************************************************************
*************************************************************************
***  Made by Facundo Diaz - August 2021                               ***
***                                                                   ***
*** END-POINTS: 1- /test/validar_pin                                  ***
***             2- /test/generar_usuario                              ***
***             3- /test/login                                        ***
***             4- /test/generar_admin                                ***
***             5- /test                                              ***
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


#Importo libraries
from datetime import datetime
import string
import random
from flask_mysqldb import MySQL
import pyotp
from flask import *
from flask_cors import CORS
import jwt
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
    #user = request.form['user']
    #pin = request.form['pin']
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


"""****************************************************************************

GENERATE A NEW USER
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

"""*************************************************************************

LOGIN
-----------
This endpoint receives user and password by parameter,
we check that they are not empty or null, then we bring
the password that corresponds to that user from the database,
if it matches, return jwt token to check on the frontend that the session is correct
and someone who did not pass the login does not access,
if they do not match or any of the checks are not successful, it returns False

*****************************************************************************"""

@app.route("/test/login", methods=["GET", "POST"])
def c():
    # user = request.form['usuario']
    # password = request.form['password']
    user = str(request.args.get('user'))
    password = str(request.args.get('password'))
    if user != "" and user != None and password != "" and password != None:
        pass_bdd = traer_password(user)
        if password == pass_bdd:
            payload_data = {"user": user,
                            "estado": True}
            key_random = str(generar_key_random())
            token = jwt.encode(payload=payload_data, key=key_random)
            return token
    return "False"

"""********************************************************************************

MAKE NEW ADMIN
------------------------
This endpoint receives by parameter the username
and password of the new system administrator that you want
to create, it is checked that it is not empty or null,
then it is checked that there is not an equal user registered in the database,
if it does not exist, we encrypt the password and save the new user in the database
and then return success, if any of the checks fails or there is a user
with that name, it returns Error

**********************************************************************************"""

@app.route("/test/generar_admin", methods=["GET", "POST"])
def d():
    # user = request.form['usuario']
    # password = request.form['password']
    user = str(request.args.get('user'))
    password = str(request.args.get('password'))
    if user != "" and user != None and password != "" and password != None:
        resultado = chequear_admin_existente(user)
        if resultado:
            return "Error"
        else:
            password = enc(password)
            guardar_admin(user, password)
            return "Success"
    return "Error"


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
def chequear_admin_existente(user):
    consulta = mysql.connection.cursor()
    consulta.execute("SELECT * FROM usuarios WHERE usuario='" + user + "';")
    resultado = consulta.fetchall()
    return resultado

"""

"""
def guardar_admin(user, password):
    sql = "INSERT INTO usuarios (usuario, password) VALUES ('" + user + "', '" + password + "');"
    consulta = mysql.connection.cursor()
    consulta.execute(sql)
    mysql.connection.commit()

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

"""

"""
def generar_key_random():
    length_of_string = 10
    return (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))

"""****************************

RUNNING FLASK SERVICES

*****************************"""
if __name__ == "__main__":
    # para correr en localhost usar este
    app.run(host='0.0.0.0')
    # para correr en servidor usar este
    #app.run(host='0.0.0.0, port=8080)
    
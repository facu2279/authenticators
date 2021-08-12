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
import re
import pyotp
from flask import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# diccionario de prueba para hacer testeos hasta agregar database
usuarios = {
    "fdiaz":"2U5EFSHZEYUE5KLL56H2DASNLMUT3HJN",
    "test1":"XAD7IP5YHH5S7ML5DPZJI55D6JBLSKEY",
    "test2":"WN3TNXM75D5N234NHFTDXSDFCGWRYCTM",
    "test3":"AE7ZT2QLKLY2WR4NJM3ID3FG3O5BGNSF",
    "TESTING": "VLGAJEKSHSQ4HOYNLOX4TT6CYNBXZLRF"
    }

# homepage route to check
@app.route("/")
def index():
    return "Online"

""" """
@app.route("/lorenzo/validar_pin", methods=["GET", "POST"])
def a():
    user = str(request.args.get('user'))
    pin = str(request.args.get('pin'))
    if user in usuarios.keys():
        secret_key_user = usuarios[user]
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
@app.route("/lorenzo/generar_usuario", methods=["GET", "POST"])
def bebe():
 
    if request.method == "POST":
        dict_to_bdd = {}
        user = str(request.args.get('user'))
        # user = request.form['usuario']
        if user in usuarios.keys():
            return "Este usuario ya tiene un qr activo"
        else:
            secret_key = pyotp.random_base32()
            qr = str(pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="App_Testing"))
            dict_to_bdd['user'] = user
            dict_to_bdd['secret_key'] = str(secret_key)
            dict_to_bdd['qr'] = qr
            fecha = datetime.now()
            fecha = fecha.strftime("%Y-%m-%d")
            dict_to_bdd['fecha'] = fecha
            usuarios[user] = secret_key
            print(dict_to_bdd)
            return str(qr)

@app.route("/lorenzo/print", methods=["GET", "POST"])
def c():
    return usuarios

# running flask server
if __name__ == "__main__":
    # para correr en localhost usar este
    app.run(host='0.0.0.0')
    # para correr en servidor usar este
    #app.run(host='0.0.0.0, port=8080)
    
from datetime import datetime
import pyotp
from flask import *
app = Flask(__name__)

"""****************************************************************
*******************************************************************
***  Made by Facundo Diaz - August 2021                         ***
***                                                             ***
***  Documentation abour PyOTP Library                          ***
***  https://pyauth.github.io/pyotp/                            ***
***                                                             ***
***                                                             ***
*******************************************************************
****************************************************************"""

# diccionario de prueba para hacer testeos hasta agregar database
usuarios = {
    "caraque":"2U5EFSHZEYUE5KLL56H2DASNLMUT3HJN",
    "fadiaz":"XAD7IP5YHH5S7ML5DPZJI55D6JBLSKEY",
    "pepe":"WN3TNXM75D5N234NHFTDXSDFCGWRYCTM",
    "scalvete":"AE7ZT2QLKLY2WR4NJM3ID3FG3O5BGNSF",
    "TESTING": "VLGAJEKSHSQ4HOYNLOX4TT6CYNBXZLRF"
    }

# homepage route to check
@app.route("/")
def index():
    return "Online"

"""
    Recive por parametros la secret key y el pin a validar
    Retorna true or false
"""
@app.route("/lorenzo/validar_pin", methods=["GET", "POST"])
def a():
    """ Hacer consulta a base de datos con el nombre de usuario para poder extraer secret key
    """
    # capturo el user y pin que me pasan por url
    user = str(request.args.get('user'))
    pin = str(request.args.get('pin'))
    #chequeo si existe el user en el diccionario (borrar cuando se agregue db)
    if user in usuarios.keys():
        #cargo secret key que le corresponde a este user
        secret_key_user = usuarios[user]
        #si existe el pin, osea que me pasaron un pin
        if pin:
            #si existe la secret key
            if (secret_key_user):
                #creo el objecto de tipo top que corresponde con el user que me pasaron
                totp = pyotp.TOTP(secret_key_user)
                #verifico si el pin del usuario coincide con el de mi objeto en este tiempo y retorno
                return str(totp.verify(pin))
            else:
                return "Error"
        else:
            return "Ingrese un pin a validar"
    else:
        return "Usuario no valido"

"""
Recibe el user por url y genero el string para que creen el qr

En issuer_name va el nombre de la app que va aparecer en la aplicacion authenticator

En dict_to_bdd se guarda, nombre del usuario, secret key, fecha y qr para guardar en base de datos

Retorno un string para generar qr
"""
@app.route("/lorenzo/generar_usuario", methods=["GET", "POST"])
def b():
    #creo el diccionario para ir guardando los datos y desp hacer consulta sql
    dict_to_bdd = {}
    #capturo el user que me pasan por url
    user = str(request.args.get('user'))
    #chequeo que exista el usuario en mis usuarios registrados
    if user in usuarios.keys():
        #si existe, no lo creo y retorno mensaje
        return "Este usuario ya tiene un qr activo"
    else:
        #si el usuario no existe le genero una secret key random en base32
        secret_key = pyotp.random_base32()
        #genero el codigo qr para este usuario
        qr = str(pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="Lorenzo"))
        #guardo datos en el diccionario para despues guardar en base de datos
        dict_to_bdd['user'] = user
        dict_to_bdd['secret_key'] = str(secret_key)
        dict_to_bdd['qr'] = qr
        #fecha de creacion (actual)
        fecha = datetime.now()
        #cambio el formato de la fecha para que sea compatible con la de sql
        fecha = fecha.strftime("%Y-%m-%d")
        dict_to_bdd['fecha'] = fecha
        #dejar esto para poder tener usuarios registrados hasta que no se agregue bdd
        usuarios[user] = secret_key
        return qr

@app.route("/lorenzo/print", methods=["GET", "POST"])
def c():
    #printea diccionario con usuarios que esten registrados, solo para testeo
    return usuarios

# running flask server
if __name__ == "__main__":
    # para correr en localhost usar este
    app.run(host='0.0.0.0')
    # para correr en servidor usar este
    #app.run(host='0.0.0.0, port=8080)
    
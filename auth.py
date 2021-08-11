import pyotp
from flask import *


app = Flask(__name__)


# homepage route
@app.route("/")
def index():
    return "<h1>Hello World!</h1>"

"""
    Recive por parametros la secret key y el pin a validar
    Returna true or false
"""
@app.route("/lorenzo/validate_pin", methods=["GET", "POST"])
def a():
    secret_key_user = str(request.args.get('sec_key'))
    pin = str(request.args.get('pin'))
    if (secret_key_user != None and pin != None):
        totp = pyotp.TOTP(secret_key_user)
        return str(totp.verify(pin))
    else:
        return "Error"

"""
Recibe el user por url y genero el string para que creen el qr
En issuer_name va el nombre de la app que va aparecer en la aplicacion authenticator
"""
@app.route("/lorenzo/generar_user", methods=["GET", "POST"])
def b():
    dict = {}
    user = str(request.args.get('user'))
    secret_key = pyotp.random_base32()
    dict['secret_key'] = str(secret_key)
    dict['codigo_para_qr']= pyotp.totp.TOTP(secret_key).provisioning_uri(name=user, issuer_name="Lorenzo")
    return dict

# running flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=8080)
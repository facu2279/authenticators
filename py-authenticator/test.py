
from flask import *
from flask_bootstrap import Bootstrap

# configuring flask application
app = Flask(__name__)

# homepage route
@app.route("/")
def index():
    return "true"


# login page route
@app.route("/lorenzo/API/v1/validate_pin", methods=["GET", "POST"])
def a():
    res = False
    val1 = str(request.args.get('user'))
    val2 = str(request.args.get('pin'))

    error = 0
    nombre = "Facundo"
    apellido = "Diaz"
    if val1 == "fadiaz":
        if val2 == "123456":
            res = True
    
    dict = {'Cod-error': error, 'Nombre': nombre,'Apellido': apellido, 'Res': res}
    return dict



# running flask server
if __name__ == "__main__":
    app.run(debug=True)
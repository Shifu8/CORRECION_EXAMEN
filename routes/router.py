from flask import Blueprint, abort , request, render_template, redirect, url_for, jsonify
from flask import flash
from flask import Flask
from controls.expresionDaoControl import ExpresionDaoControl
from models.expresion import Expresion
from controls.expresionControl import ExpresionControl
from flask_cors import CORS
import json


app = Flask(__name__)
app.secret_key = '1234'

cors = CORS(app)

router = Blueprint('router', __name__)

import secrets

app.secret_key = secrets.token_hex(16)  # Genera una cadena hexadecimal de 16 bytes



#CORS(api)
cors = CORS(router, resource={
    r"/*":{
        "origins":"*"
    }
})

@router.route('/') #SON GETS
def home():
    return render_template('templateexpresiones.html')

@router.route('/expresiones')
def lista_expresion():
    ed = ExpresionDaoControl()
    return render_template('expresiones/listaexpresiones.html', lista = ed.to_dict())

@router.route('/expresiones/ver')
def ver_expresiones():
   return render_template('expresiones/guardarexpresiones.html')


@router.route('/expresiones/guardar', methods=["POST"])
def guardar_expresiones():
    ed = ExpresionDaoControl()
    data = request.form

    if not all(key in data for key in ["expresion", "resultado"]):
        abort(400, "Faltan datos necesarios")

    nueva_expresion = Expresion()
    nueva_expresion._expresion = str(data["expresion"])
    nueva_expresion._resultado = str(data["resultado"])
    

    lista_expresiones = ed._list()
    nuevo_id = lista_expresiones._lenght + 1  # ID único basado en la longitud de la lista más 1
    nueva_expresion._id = nuevo_id

    ed._save(nueva_expresion)

    return redirect("/expresiones", code=302)

@app.route('/calcular_expresion', methods=['GET', 'POST'])
def calcular_expresion():
    if request.method == 'POST':
        data = request.json
        expresion = data['expresion']
        print('Expresión recibida:', expresion)  # Mensaje de depuración en el servidor
        # Aquí llamamos a tu método para calcular la expresión
        expresion_dao_control = ExpresionDaoControl()
        resultado = expresion_dao_control.calcular_expresion(expresion)
        print('Resultado calculado:', resultado)  # Mensaje de depuración en el servidor
        return jsonify({'resultado': resultado})
    else:
        expresion = request.args.get('expresion')
        return render_template('calcularexpresion.html', expresion=expresion)


@router.route('/expresiones/eliminar/<int:expresion_id>', methods=["POST"])
def eliminar_expresion(expresion_id):
    ec = ExpresionControl()
    try:
        ec.eliminar(expresion_id)
        
        with open('data/expresion.json', 'r') as file:
            expresiones = json.load(file)
        expresiones = [expresion for expresion in expresiones if expresion['id'] != expresion_id]
        with open('data/expresion.json', 'w') as file:
            json.dump(expresiones, file, indent=4)

        return jsonify({"message": "Expresion eliminada correctamente.", "expresion_id": expresion_id}), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo eliminar la expresion: {str(e)}"}), 500
 

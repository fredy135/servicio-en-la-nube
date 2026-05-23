import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calcular', methods=['POST'])
def calcular_interes():
    datos = request.get_json()
    
    # Extraemos los datos enviados por el frontend
    monto = float(datos.get('monto', 0))
    tasa_anual = float(datos.get('tasa', 0))
    
    # Lógica de la app (Capa 2)
    interes_mensual = (monto * (tasa_anual / 100)) / 12
    total_pagar = monto + (interes_mensual * 12) # Simulación a un año
    
    # Respondemos al frontend con un JSON limpio
    return jsonify({
        "interes_mensual": round(interes_mensual, 2),
        "total_pagar": round(total_pagar, 2)
    })

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)


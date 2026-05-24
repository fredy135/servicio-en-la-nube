import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

DB_FILE = 'banco.db'

def init_db():
    """Crea la tabla en la base de datos si no existe al arrancar el servidor"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL NOT NULL,
            tasa REAL NOT NULL,
            interes_mensual REAL NOT NULL,
            total_pagar REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializamos la base de datos 
init_db()

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        monto = float(data.get('monto', 0))
        tasa = float(data.get('tasa', 0))
        
        interes_mensual = (monto * (tasa / 100)) / 12
        total_pagar = monto + (interes_mensual * 12)
        
        interes_mensual = round(interes_mensual, 2)
        total_pagar = round(total_pagar, 2)
        
        #persistencia con SQLITE
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historial (monto, tasa, interes_mensual, total_pagar)
            VALUES (?, ?, ?, ?)
        ''', (monto, tasa, interes_mensual, total_pagar))
        conn.commit()
        conn.close()
        
        # Responder al Frontend
        return jsonify({
            "monto": monto,
            "tasa": tasa,
            "interes_mensual": interes_mensual,
            "total_pagar": total_pagar
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/historial', methods=['GET'])
def obtener_historial():
    """Ruta extra para comprobar la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT monto, tasa, interes_mensual, total_pagar FROM historial ORDER BY id DESC')
    filas = cursor.fetchall()
    conn.close()
    
    # Formateamos los datos como una lista de diccionarios JSON
    historial = []
    for fila in filas:
        historial.append({
            "monto": fila[0],
            "tasa": fila[1],
            "interes_mensual": fila[2],
            "total_pagar": fila[3]
        })
        
    return jsonify(historial)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/add-user', methods=['POST'])
def add_user():
    connection = None
    cursor = None
    try:
        # Obtener datos del cuerpo de la solicitud
        user_data = request.get_json()
        nombre = user_data['nombre']
        email = user_data['email']
        
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='172.31.84.130',
            user='flask_user',
            password='pws1234!',
            database='baseparcial'
        )

        # Inserción de datos en la tabla
        if connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
            cursor.execute(query, (nombre, email))
            connection.commit()
            return jsonify({
                "status": "success",
                "message": "Usuario añadido con éxito"
            })

    except Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error al añadir usuario: {e}"
        })

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
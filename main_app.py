from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import hashlib  # Para encriptar la contraseña
from flask_cors import CORS

app = Flask(__name__)

# Configura CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Permite solicitudes de cualquier origen

# Ruta para añadir un nuevo usuario (POST)
@app.route('/add-user', methods=['POST'])
def add_user():
    connection = None
    cursor = None
    try:
        # Obtener datos del cuerpo de la solicitud
        user_data = request.get_json()
        nombres = user_data['nombres']
        apellidos = user_data['apellidos']
        fecha_nacimiento = user_data['fecha_nacimiento']
        password = user_data['password']

        # Encriptar la contraseña usando SHA-256
        password_encriptada = hashlib.sha256(password.encode()).hexdigest()
        
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
            query = """
                INSERT INTO usuarios (nombres, apellidos, fecha_nacimiento, password)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombres, apellidos, fecha_nacimiento, password_encriptada))
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

# Ruta para obtener todos los usuarios (GET)
@app.route('/get-users', methods=['GET'])
def get_users():
    connection = None
    cursor = None
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host='172.31.84.130',
            user='flask_user',
            password='pws1234!',
            database='baseparcial'
        )

        # Consulta para obtener los datos de los usuarios
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, nombres, apellidos, fecha_nacimiento FROM usuarios"
            cursor.execute(query)
            usuarios = cursor.fetchall()

            return jsonify({
                "status": "success",
                "data": usuarios
            })

    except Error as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener usuarios: {e}"
        })

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/test-db-connection')
def test_db_connection():
    connection = None
    cursor = None
    try:
        # Intento de conexión a la base de datos MySQL
        connection = mysql.connector.connect(
            host='172.31.84.130',  # IP privada de tu servidor MySQL
            user='flask_user',  # Usuario de la base de datos
            password='pws1234!',  # Contraseña de la base de datos
            database='baseparcial'  # Nombre de la base de datos
        )

        # Verifica si la conexión es exitosa
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db = cursor.fetchone()
            return jsonify({
                "status": "success",
                "message": "Conexión exitosa a la base de datos",
                "database": db[0]
            })

    except Error as e:
        # Manejador de errores si la conexión falla
        return jsonify({
            "status": "error",
            "message": f"Error al conectar a la base de datos: {e}"
        })

    finally:
        # Cierra cursor y conexión si están definidos y conectados
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

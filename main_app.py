from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import boto3
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configura CORS
CORS(app)

# Configura la conexión a la base de datos RDS usando variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Condición para evitar la conexión en modo de pruebas
if not app.testing:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuración de credenciales de AWS para Athena usando variables de entorno
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
REGION_NAME = 'us-east-1'

# Inicializar el cliente de Athena
athena_client = boto3.client(
    'athena',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

ATHENA_DATABASE = 's3_sakila'
ATHENA_OUTPUT_LOCATION = 's3://s3sakila/'


# Verificar la conexión a la base de datos


# Ruta para añadir una nueva renta y manejar todas las inserciones
@app.route('/add-rental', methods=['POST'])
def add_rental():
    try:
        # Obtener datos de la solicitud
        rental_date = request.get_json().get('rental_date')
        customer_id = request.get_json().get('customer_id')
        film_id = request.get_json().get('film_id')

        if not all([rental_date, customer_id, film_id]):
            return jsonify({
                "status": "error",
                "message": "Campos 'rental_date', 'customer_id' y 'film_id' son obligatorios"
            }), 400

        # 1. Obtener o insertar el address_id del cliente
        address_query = text("""
            SELECT address_id FROM customer WHERE customer_id = :customer_id
        """)
        address_id = db.session.execute(address_query, {'customer_id': customer_id}).scalar()

        if not address_id:
            address_insert = text("""
                INSERT INTO address (address, district, city_id, postal_code, phone, last_update)
                VALUES ('Default Address', 'Default District', 1, '00000', '000-0000', NOW())
            """)
            db.session.execute(address_insert)
            address_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            update_customer_address = text("""
                UPDATE customer SET address_id = :address_id WHERE customer_id = :customer_id
            """)
            db.session.execute(update_customer_address, {'address_id': address_id, 'customer_id': customer_id})

        # 2. Verificar o insertar el inventario para la película
        inventory_query = text("""
            SELECT inventory_id FROM inventory WHERE film_id = :film_id LIMIT 1
        """)
        inventory_id = db.session.execute(inventory_query, {'film_id': film_id}).scalar()

        if not inventory_id:
            inventory_insert = text("""
                INSERT INTO inventory (film_id, store_id, last_update)
                VALUES (:film_id, 1, NOW())
            """)
            db.session.execute(inventory_insert, {'film_id': film_id})
            inventory_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        # 3. Crear la renta en la tabla rental
        rental_insert = text("""
            INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id, return_date, last_update)
            VALUES (:rental_date, :inventory_id, :customer_id, 1, NULL, NOW())
        """)
        db.session.execute(rental_insert, {
            'rental_date': rental_date,
            'inventory_id': inventory_id,
            'customer_id': customer_id
        })
        rental_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        # 4. Inserción en la tabla payment
        payment_insert = text("""
            INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date, last_update)
            VALUES (:customer_id, 1, :rental_id, 4.99, NOW(), NOW())
        """)
        db.session.execute(payment_insert, {
            'customer_id': customer_id,
            'rental_id': rental_id
        })

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Renta y registros relacionados añadidos con éxito"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"Error al añadir la renta: {e}"
        })


# Ruta para obtener las películas rentadas por un cliente con el nombre de la película (GET)
@app.route('/get-movies/<int:id_customer>', methods=['GET'])
def get_movies(id_customer):
    query = f"""
        SELECT fv.customer_id, fv.film_id, f.title, fv.rental_date
        FROM fact_venta fv
        JOIN film f ON fv.film_id = f.film_id
        WHERE fv.customer_id = {id_customer}
        ORDER BY fv.rental_date DESC  -- Orden ascendente por fecha de inserción
    """


    try:
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': ATHENA_DATABASE},
            ResultConfiguration={'OutputLocation': ATHENA_OUTPUT_LOCATION}
        )

        query_execution_id = response['QueryExecutionId']

        # Esperar a que la consulta se complete
        status = 'RUNNING'
        while status in ['RUNNING', 'QUEUED']:
            response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)

        if status == 'SUCCEEDED':
            results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
            ventas = []
            for row in results['ResultSet']['Rows'][1:]:
                customer_id = row['Data'][0]['VarCharValue']
                film_id = row['Data'][1]['VarCharValue']
                title = row['Data'][2]['VarCharValue']
                rental_date = row['Data'][3]['VarCharValue']
                ventas.append({
                    'customer_id': customer_id,
                    'film_id': film_id,
                    'title': title,
                    'rental_date': rental_date,
                })

            return jsonify({
                "status": "success",
                "data": ventas
            })
        else:
            return jsonify({
                "status": "error",
                "message": "La consulta a Athena falló o fue cancelada"
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener datos de ventas: {e}"
        })


# Ruta para obtener todas las películas (GET)
@app.route('/movies', methods=['GET'])
def get_all_movies():
    query = "SELECT film_id, title FROM film"

    try:
        movies = db.session.execute(text(query)).fetchall()
        movies_list = [{'film_id': film_id, 'title': title} for film_id, title in movies]

        return jsonify({
            "status": "success",
            "data": movies_list
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error al obtener las películas: {e}"
        })


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

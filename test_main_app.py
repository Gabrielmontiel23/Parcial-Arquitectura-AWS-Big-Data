import unittest
from main_app import app
from flask import g
import sqlite3

class TestMainApp(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
        self.client = app.test_client()

        with app.app_context():
            self.init_db()  # Inicializa la base de datos con las tablas necesarias

    def init_db(self):
        # Crea una conexión SQLite y crea las tablas necesarias para las pruebas
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        g._database = conn  # Asigna la conexión a la base de datos al contexto de la aplicación

    def test_add_user(self):
        # Prueba para la ruta /add-user
        response = self.client.post('/add-user', json={
            'nombres': 'Maria',
            'apellidos': 'Pérez',
            'fecha_nacimiento': '1990-01-01',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario añadido con éxito', response.get_json().get('message', ''))
        print('Usuario añadido con éxito:', response.get_json().get('message', ''))

    def test_get_users(self):
        # Inserta un usuario de prueba antes de la solicitud
        with app.app_context():
            cursor = g._database.cursor()
            cursor.execute('INSERT INTO usuarios (nombres, apellidos, fecha_nacimiento, password) VALUES (?, ?, ?, ?)',
                           ('Juan', 'Díaz', '1985-07-15', 'secret'))
            g._database.commit()

        # Prueba para la ruta /get-users
        response = self.client.get('/get-users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get('status'), 'success')
        # Verificar que la respuesta contenga una lista
        self.assertIsInstance(response.get_json().get('data'), list)
        print('Usuarios obtenidos:', response.get_json().get('data'))

if __name__ == '__main__':
    unittest.main()

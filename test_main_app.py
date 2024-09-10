import unittest
import tempfile
import os
from main_app import app
from flask_sqlalchemy import SQLAlchemy

class TestMainApp(unittest.TestCase):

    def setUp(self):
        # Crear una base de datos temporal en memoria
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        self.client = app.test_client()

        # Crear las tablas en la base de datos temporal
        with app.app_context():
            db = SQLAlchemy(app)
            db.create_all()

    def tearDown(self):
        # Cerrar y eliminar la base de datos temporal
        os.close(self.db_fd)
        os.unlink(self.db_path)

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

    def test_get_users(self):
        # Prueba para la ruta /get-users
        response = self.client.get('/get-users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get('status'), 'success')
        self.assertIsInstance(response.get_json().get('data'), list)

if __name__ == '__main__':
    unittest.main()

# test_main_app.py
import unittest
from main_app import app, db

class TestMainApp(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usar SQLite en memoria
        self.client = app.test_client()
        
        # Crear todas las tablas
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Eliminar todas las tablas después de cada prueba
        with app.app_context():
            db.session.remove()
            db.drop_all()

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
        print('Usuario añadido con éxito', response.get_json().get('message', ''))

    def test_get_users(self):
        # Prueba para la ruta /get-users
        response = self.client.get('/get-users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get('status'), 'success')
        # Verificar que la respuesta contenga una lista
        self.assertIsInstance(response.get_json().get('data'), list)
        print(response.get_json().get('data'), list)

if __name__ == '__main__':
    unittest.main()

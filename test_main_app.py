import unittest
from main_app import app, db

class TestMainApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['DATABASE'] = 'test_database.db'
        cls.client = cls.app.test_client()

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_add_user(self):
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
        # Primero añadir un usuario para comprobar
        self.client.post('/add-user', json={
            'nombres': 'Maria',
            'apellidos': 'Pérez',
            'fecha_nacimiento': '1990-01-01',
            'password': 'password123'
        })
        response = self.client.get('/get-users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get('status'), 'success')
        self.assertIsInstance(response.get_json().get('data'), list)
        print(response.get_json().get('data'), list)

if __name__ == '__main__':
    unittest.main()

import unittest
import json
from main_app import app, db  # Asegúrate de que main_app.py esté en el mismo directorio o especifica el path correctamente

class MainAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuración inicial para ejecutar las pruebas
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Limpia la base de datos después de todas las pruebas
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_rental_missing_fields(self):
        """Prueba para el endpoint /add-rental con campos faltantes"""
        response = self.client.post('/add-rental', json={
            'rental_date': '2024-01-01',
            'customer_id': 1  # Falta film_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json['status'])

    def test_add_rental_successful(self):
        """Prueba para el endpoint /add-rental con datos correctos"""
        response = self.client.post('/add-rental', json={
            'rental_date': '2024-01-01',
            'customer_id': 1,
            'film_id': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json['status'])

    def test_get_movies_for_customer(self):
        """Prueba para el endpoint /get-movies/<id_customer>"""
        response = self.client.get('/get-movies/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json['status'])
        self.assertIsInstance(response.json['data'], list)

    def test_get_all_movies(self):
        """Prueba para el endpoint /movies"""
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json['status'])
        self.assertIsInstance(response.json['data'], list)

    def test_get_movies_invalid_customer(self):
        """Prueba para verificar manejo de errores en /get-movies/<id_customer>"""
        response = self.client.get('/get-movies/9999')  # Cliente inexistente
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json['status'])  # Puede cambiar según implementación

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from flask import json
from main_app import app  # Cambia 'main_app' al nombre real de tu módulo o archivo

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar el cliente de prueba de Flask
        cls.app = app.test_client()
        cls.app.testing = True

    # Prueba para el endpoint /add-rental con base de datos simulada
    @patch('main_app.db.session')
    def test_add_rental_success(self, mock_session):
        # Simular el comportamiento de la base de datos
        mock_session.execute.return_value = MagicMock(scalar=MagicMock(return_value=1))

        # Datos de prueba para añadir una renta
        rental_data = {
            "rental_date": "2024-10-24 14:30:00",
            "customer_id": 5,
            "film_id": 1
        }
        
        # Realizar la solicitud POST
        response = self.app.post('/add-rental', 
                                 data=json.dumps(rental_data),
                                 content_type='application/json')

        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Renta y registros relacionados añadidos con éxito')
        self.assertTrue(mock_session.execute.called)
        self.assertTrue(mock_session.commit.called)

    # Prueba para el endpoint /get-movies/<id_customer> con AWS Athena simulado
    @patch('main_app.athena_client.start_query_execution')
    @patch('main_app.athena_client.get_query_execution')
    @patch('main_app.athena_client.get_query_results')
    def test_get_movies_success(self, mock_get_query_results, mock_get_query_execution, mock_start_query_execution):
        # Simular el inicio de la consulta
        mock_start_query_execution.return_value = {'QueryExecutionId': '1234'}
        # Simular que la consulta en Athena fue exitosa
        mock_get_query_execution.return_value = {
            'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}
        }
        # Simular los resultados de la consulta
        mock_get_query_results.return_value = {
            'ResultSet': {
                'Rows': [
                    {'Data': [{'VarCharValue': '5'}, {'VarCharValue': '1'}, {'VarCharValue': 'Inception'}, {'VarCharValue': '2024-10-24 14:30:00'}]},
                ]
            }
        }
    
        # Realizar la solicitud GET
        response = self.app.get('/get-movies/5')
    
        # Verificar que la respuesta sea exitosa y contenga un elemento
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 1)  # Se espera un elemento en 'data'
        self.assertEqual(response_json['data'][0]['title'], 'Inception')


    # Prueba para el endpoint /movies con base de datos simulada
    @patch('main_app.db.session')
    def test_get_all_movies_success(self, mock_session):
        # Simular el resultado de la consulta SQL
        mock_session.execute.return_value.fetchall.return_value = [
            (1, 'Inception'),
            (2, 'Interstellar')
        ]

        # Realizar la solicitud GET
        response = self.app.get('/movies')

        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 2)
        self.assertEqual(response_json['data'][0]['title'], 'Inception')
        self.assertTrue(mock_session.execute.called)

if __name__ == '__main__':
    unittest.main()

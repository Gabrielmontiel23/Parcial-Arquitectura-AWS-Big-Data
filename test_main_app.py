import unittest
from unittest.mock import patch, MagicMock
from flask import json
from main_app import app

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    @patch('main_app.db.session.execute')
    @patch('main_app.db.session.commit')
    def test_add_rental_success(self, mock_commit, mock_execute):
        # Simula las inserciones en la base de datos con mocks
        mock_execute.return_value.scalar.side_effect = [1, 2, 3]  # IDs simulados para address, inventory, rental
        
        # Datos de prueba para la solicitud POST
        rental_data = {
            'rental_date': '2024-10-24 14:30:00',
            'customer_id': 5,
            'film_id': 1
        }

        response = self.app.post('/add-rental', 
                                 data=json.dumps(rental_data),
                                 content_type='application/json')

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(response_json['message'], 'Renta y registros relacionados añadidos con éxito')

    @patch('main_app.athena_client.start_query_execution')
    @patch('main_app.athena_client.get_query_execution')
    @patch('main_app.athena_client.get_query_results')
    def test_get_movies_success(self, mock_get_query_results, mock_get_query_execution, mock_start_query_execution):
        # Simula la ejecución de la consulta en Athena
        mock_start_query_execution.return_value = {'QueryExecutionId': '1234'}
        mock_get_query_execution.return_value = {
            'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}
        }
        
        # Ajuste del mock para get_query_results
        mock_get_query_results.return_value = {
            'ResultSet': {
                'Rows': [
                    {'Data': [{'VarCharValue': 'customer_id'}, {'VarCharValue': 'film_id'}, {'VarCharValue': 'title'}, {'VarCharValue': 'rental_date'}]},  # Fila de encabezado
                    {'Data': [{'VarCharValue': '5'}, {'VarCharValue': '1'}, {'VarCharValue': 'Inception'}, {'VarCharValue': '2024-10-24 14:30:00'}]},
                    {'Data': [{'VarCharValue': '5'}, {'VarCharValue': '2'}, {'VarCharValue': 'The Matrix'}, {'VarCharValue': '2024-10-25 14:30:00'}]},
                ]
            }
        }


        # Realiza la solicitud GET
        response = self.app.get('/get-movies/5')

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 2)
        self.assertEqual(response_json['data'][0]['title'], 'Inception')
        self.assertEqual(response_json['data'][1]['title'], 'The Matrix')

    @patch('main_app.db.session.execute')
    def test_get_all_movies_success(self, mock_execute):
        # Simula los resultados de la consulta a la base de datos
        mock_execute.return_value.fetchall.return_value = [
            (1, 'ACADEMY DINOSAUR'), 
            (2, 'THE MATRIX')
        ]

        # Realiza la solicitud GET
        response = self.app.get('/movies')

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['status'], 'success')
        self.assertEqual(len(response_json['data']), 2)
        self.assertEqual(response_json['data'][0]['title'], 'ACADEMY DINOSAUR')
        self.assertEqual(response_json['data'][1]['title'], 'THE MATRIX')

if __name__ == '__main__':
    unittest.main()

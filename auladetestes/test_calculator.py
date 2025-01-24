import unittest
from app import app

class TestCalculator(unittest.TestCase):

    def setUp(self):
        # Cria um cliente de teste para enviar requisições
        self.client = app.test_client()

    def test_valid_expression(self):
        # Testa uma expressão válida
        response = self.client.post('/', data={'expression': '2+2'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'4', response.data)  # Verifica se o resultado contém '4'

    def test_invalid_expression(self):
        # Testa uma expressão inválida
        response = self.client.post('/', data={'expression': '2/0'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)  # Verifica se contém 'Error'

    def test_empty_expression(self):
        # Testa quando não é passada nenhuma expressão
        response = self.client.post('/', data={'expression': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)  # Verifica se contém 'Error'

    def test_negative_numbers(self):
        response = self.client.post('/', data={'expression': '-5+3'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'-2', response.data)  # Resultado esperado é '-2'

    def test_expression_with_parentheses(self):
        response = self.client.post('/', data={'expression': '(2+3)*4'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'20', response.data)  # Resultado esperado é '20'

    def test_float_division(self):
        response = self.client.post('/', data={'expression': '5/2'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2.5', response.data)  # Resultado esperado é '2.5'

    def test_multiple_operators(self):
        response = self.client.post('/', data={'expression': '2+3*4-1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'13', response.data)  # Respeita a precedência: 2+(3*4)-1 = 13

    def test_long_expression(self):
        response = self.client.post('/', data={'expression': '1+2+3+4+5+6+7+8+9'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'45', response.data)  # Resultado esperado é '45'

    def test_expression_with_spaces(self):
        response = self.client.post('/', data={'expression': '  2 + 3 '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'5', response.data)  # Resultado esperado é '5'

    def test_operations_with_zero(self):
        response = self.client.post('/', data={'expression': '0*10'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'0', response.data)  # Resultado esperado é '0'

    def test_non_numeric_input(self):
        response = self.client.post('/', data={'expression': 'abc+123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)  # Deve retornar um erro

    def test_large_numbers(self):
        response = self.client.post('/', data={'expression': '999999999+1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1000000000', response.data)  # Resultado esperado é '1000000000'


if __name__ == '__main__':
    unittest.main()

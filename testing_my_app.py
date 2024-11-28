import unittest

from projects import create_app


class MpesaApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_mpesa_api(self):
        pdf_path = ''
        with open(pdf_path, 'rb') as f:
            response = self.client.post(
                '/mpesa/mpesa_api',
                data={
                    'pdf': (f, 'testfile.pdf'),
                    'password': ''
                }
            )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response is a JSON object
        self.assertEqual(response.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
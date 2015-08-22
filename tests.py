import os
from   app import app
import unittest
import json
import urllib3

class ClientAPI(object):
    def __init__(self):
        self.http = urllib3.PoolManager()

    def request(self, method, url):
        
        response = self.http.request(method,url)

        raw_data = response.read().decode('utf-8')
        return json.loads(raw_data)

class RedilTestCase(unittest.TestCase):

    def setUp(self):
        self.client = ClientAPI
        self.app = app.test_client()

    def test_json_404(self):
        response = self.app.get('/urlinexistente')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('error',json_response)
        self.assertEqual('Not found',json_response['error'])

    def test_api_get_all_documents(self):
        response = self.app.get('/api/v1/documents')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('documents',json_response)
        self.assertIs(list,type(json_response['documents']))

    def test_api_search_documents(self):
        response = self.app.get('/api/v1/documents?search_string=parasauro')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('documents',json_response)
        self.assertIs(list,type(json_response['documents']))

if __name__ == '__main__':
    unittest.main()

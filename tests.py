import os
from   app import create_app, db
import unittest
import json
import urllib3

class RedilTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.environ["APP_SETTINGS"] = "config.TestingConfig"
        app = create_app()
        app.app_context().push()
        db.create_all()
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()

    def test_json_404(self):
        response = self.app.get('/urlinexistente')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('error',json_response)
        self.assertEqual(404,json_response['error'])
        self.assertEqual(response.status_code,404)

#    @unittest.skip("testing skipping")
    def test_api_get_all_documents(self):
        response = self.app.get('/api/v1/documents')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('documents',json_response)
        self.assertIs(list,type(json_response['documents']))
        self.assertEqual(response.status_code,200)
        

#    @unittest.skip("testing skipping")
    def test_api_search_documents(self):
        response = self.app.get('/api/v1/documents?search_string=parasauro')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('documents',json_response)
        self.assertIs(list,type(json_response['documents']))
        self.assertEqual(response.status_code,200)

    def test_api_create_document(self):
        headers = [('Content-Type', 'application/json')]
        data = {'name': 'Jesse', 'path' : 'http://localhost/testcase', 'content' : 'test case data', 'chash' : 'ertwrewrew',
                'mime': 'asdasd', 'pages': 9 , 'utility': 'popo'}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        response = self.app.put('/api/v1/documents', headers=headers, data=json_data)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code,201)
        self.assertIn('id', json_response['document'])
        self.assertIn('name', json_response['document'])
        self.assertIn('path', json_response['document'])
        self.assertIn('utility', json_response['document'])
        self.assertIn('mime', json_response['document'])
        self.assertIn('pages', json_response['document'])
        self.assertIn('uri', json_response['document'])
        self.assertIn('content', json_response['document'])
        self.assertIn('chash', json_response['document'])
        db.session.flush()

    def test_api_delete_document(self):
        response = self.app.delete('/api/v1/documents/1')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIn('result',json_response)
        self.assertEqual(json_response['result'],True)
        self.assertEqual(response.status_code,200)

if __name__ == '__main__':
    unittest.main()

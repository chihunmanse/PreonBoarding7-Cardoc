import json
import bcrypt
import jwt

from django.test     import TestCase, Client

from users.models    import User
from cardoc.settings import SECRET_KEY, ALGORITHM

class UserTest(TestCase):
    def setUp(self):
        global access_token
        user1        = User.objects.create(id = 'user1', password = bcrypt.hashpw('abc1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        access_token = jwt.encode({"user_id": user1.id}, SECRET_KEY, ALGORITHM)
    
    def tearDown(self):
        User.objects.all().delete()
    
    def test_post_sign_up_success(self):
        client = Client()
        
        data     = {'id' : 'user3', 'password' : 'abc1234'}
        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            { "message" : "SUCCESS" }
        )

    def test_post_sign_up_fail_user_already_exist(self):
        client = Client()
        
        data     = {'id' : 'user1', 'password' : 'abc1234'}
        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : 'ID_ALREADY_EXIST' }
        )

    def test_post_sign_up_fail_invalid_id(self):
        client = Client()
        
        data     = {'id' : '', 'password' : 'abc1234'}
        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : "INVALID_ID" }
        )

    def test_post_sign_up_fail_key_error(self):
        client = Client()
        
        data     = {'idd' : 'user3', 'password' : 'abc1234'}
        response = client.post('/users/signup', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : 'KEY_ERROR' }
        )

    def test_post_sign_up_fail_json_decode_error(self):
        client = Client()
        
        response = client.post('/users/signup')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : "JSON_DECODE_ERROR" }
        )

    def test_post_sign_in_success(self):
        client = Client()
        
        data     = {'id' : 'user1', 'password' : 'abc1234'}
        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            { "token" : access_token }
        )

    def test_post_sign_in_fail_user_does_noe_exist(self):
        client = Client()
        
        data     = {'id' : 'user3', 'password' : 'abc1234'}
        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            { "message" : 'USER_DOES_NOT_EXIST' }
        )

    def test_post_sign_in_fail_invalid_password(self):
        client = Client()
        
        data     = {'id' : 'user1', 'password' : 'abc123'}
        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            { "message" : 'INVALID_PASSWORD' }
        )

    def test_post_sign_in_fail_key_error(self):
        client = Client()
        
        data     = {'idd' : 'user1', 'password' : 'abc1234'}
        response = client.post('/users/signin', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : 'KEY_ERROR' }
        )

    def test_post_sign_in_fail_json_decode_error(self):
        client = Client()
        
        response = client.post('/users/signin')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            { "message" : 'JSON_DECODE_ERROR' }
        )
import jwt, json

from django.test     import TestCase, Client
from unittest.mock   import patch, MagicMock

from users.models    import User, UserTrim
from trims.models    import Trim, Tire
from cardoc.settings import SECRET_KEY, ALGORITHM

class TrimViewTest(TestCase):
    def setUp(self):
        global headers1, headers2
        user1 = User.objects.create(id = 'user1', password = 'abc1234')
        user2 = User.objects.create(id = 'user2', password = 'abc1234')

        access_token1 = jwt.encode({'user_id' : user1.id}, SECRET_KEY, ALGORITHM)
        access_token2 = jwt.encode({'user_id' : user2.id}, SECRET_KEY, ALGORITHM)
        headers1      = {'HTTP_AUTHORIZATION': access_token1}
        headers2      = {'HTTP_AUTHORIZATION': access_token2}

        tire = Tire.objects.create(id = 1, width = 225, aspect_ratio = 60, wheel_size = 16)
        trim = Trim.objects.create(id = 1, name = "GH270 고급형", front_tire = tire, rear_tire = tire)
        UserTrim.objects.create(id = 1, user = user1, trim = trim)

    def tearDown(self):
        User.objects.all().delete()
        Tire.objects.all().delete()
        Trim.objects.all().delete()
        UserTrim.objects.all().delete()
    
    @patch('trims.utils.requests')
    def test_post_success(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return {
                    "trimName": "GH270 고급형",
                    "spec": {
                        "driving": {
                            "frontTire": {"name": "타이어 전", "value": "225/60R16", "unit": "", "multiValues": ""},
                            "rearTire":  {"name": "타이어 후", "value": "225/60R16", "unit": "", "multiValues": ""},
                        }
                    },
                }
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'id'     : 'user1',
                'trimId' : 5000
            }
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'message' : 'SUCCESS'
            }
        )

    @patch('trims.utils.requests')
    def test_post_fail_too_much_request(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return {
                    "trimName": "GH270 고급형",
                    "spec": {
                        "driving": {
                            "frontTire": {"name": "타이어 전", "value": "225/60R16", "unit": "", "multiValues": ""},
                            "rearTire":  {"name": "타이어 후", "value": "225/60R16", "unit": "", "multiValues": ""},
                        }
                    },
                }
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'id'     : 'user1',
                'trimId' : 5000
            },
            {
                'id'     : 'user2',
                'trimId' : 5000
            },
            {
                'id'     : 'user3',
                'trimId' : 5000
            },
            {
                'id'     : 'user4',
                'trimId' : 5000
            },
            {
                'id'     : 'user5',
                'trimId' : 5000
            },
            {
                'id'     : 'user6',
                'trimId' : 5000
            },
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'TOO_MUCH_REQUEST'
            }
        )

    @patch('trims.utils.requests')
    def test_post_fail_invalid_trim_id(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return None
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'id'     : 'user1',
                'trimId' : 5000
            }
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_TRIM_ID'
            }
        )

    @patch('trims.utils.requests')
    def test_post_fail_invalid_tire_format(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return {
                    "trimName": "GH270 고급형",
                    "spec": {
                        "driving": {
                            "frontTire": {"name": "타이어 전", "value": "22560R16", "unit": "", "multiValues": ""},
                            "rearTire":  {"name": "타이어 후", "value": "22560R16", "unit": "", "multiValues": ""},
                        }
                    },
                }
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'id'     : 'user1',
                'trimId' : 5000
            }
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_TIRE_FORMAT'
            }
        )

    @patch('trims.utils.requests')
    def test_post_fail_key_error(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return {
                    "trimName": "GH270 고급형",
                    "spec": {
                        "driving": {
                            "frontTire": {"name": "타이어 전", "value": "225/60R16", "unit": "", "multiValues": ""},
                            "rearTire":  {"name": "타이어 후", "value": "225/60R16", "unit": "", "multiValues": ""},
                        }
                    },
                }
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'idd'    : 'user1',
                'trimId' : 5000
            }
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'KEY_ERROR'
            }
        )

    @patch('trims.utils.requests')
    def test_post_fail_invalid_user_id(self, mock_data_request):
        clinet = Client()

        class MockDataResponse:
            def json(self):
                return {
                    "trimName": "GH270 고급형",
                    "spec": {
                        "driving": {
                            "frontTire": {"name": "타이어 전", "value": "225/60R16", "unit": "", "multiValues": ""},
                            "rearTire":  {"name": "타이어 후", "value": "225/60R16", "unit": "", "multiValues": ""},
                        }
                    },
                }
            
            def raise_for_status(self):
                pass
            
        data = [
            {
                'id'     : 'user3',
                'trimId' : 5000
            }
        ]

        mock_data_request.get = MagicMock(return_value = MockDataResponse())
        
        response = clinet.post('/trims', json.dumps(data), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'INVALID_USER_ID'
            }
        )
    
    def test_get_success(self):
        clinet = Client()
            
        data = [
            {
                "trim_name": "GH270 고급형",
                "front_tire": {
                    "width": 225,
                    "aspect_ratio": 60,
                    "wheel_size": 16
                },
                "rear_tire": {
                    "width": 225,
                    "aspect_ratio": 60,
                    "wheel_size": 16
                }
            }
        ]

        response = clinet.get('/trims', **headers1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'data' : data
            }
        )
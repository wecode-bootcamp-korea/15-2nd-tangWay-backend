import unittest, json, jwt, bcrypt
from datetime      import datetime, timedelta
from django.test   import TestCase, Client
from user.models   import User, Gender, Country
from my_settings   import SECRET_KEY, JWT_ALGORITHM
from unittest.mock import patch, MagicMock

class SignUpTestCase(TestCase):
    def setUp(self):
         self.gender     = Gender.objects.create(name='male')
         self.country    = Country.objects.create(name='대한민국')
         hashed_password = bcrypt.hashpw('123456aA!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
         self.client = Client()

         User.objects.create(
                 id            = 1,
                 korean_name   = '문타리',
                 english_name  = 'munshee',
                 email         = 'applee24@gmail.com',
                 password      = hashed_password,
                 date_of_birth = '1992-04-24',
                 phone_number  = '010-9999-1234',
                 gender_id     = self.gender.id,
                 country_id    = self.country.id
                 )

    def tearDown(self):
        Gender.objects.all().delete()
        Country.objects.all().delete()
        User.objects.all().delete()

    def test_user_post_signup_success(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'kimapple',
                'email'         : 'apple92@gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1234-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
            {
                'MESSAGE':'SUCCESS'
            }
        )

    def test_user_post_signup_emailformat_validation(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'kimapple',
                'email'         : 'apple92gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1234-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'INCORRECT_EMAIL_FORMAT'
            }
        )

    def test_user_post_signup_password_validation(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'kimapple',
                'email'         : 'apple92@gmail.com',
                'password'      : '123456',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1234-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'INCORRECT_PASSWORD_FORMAT'
            }
        )

    def test_user_post_signup_email_exists_validation(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'kimapple',
                'email'         : 'applee24@gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1234-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'ALREADY_EXISTS_EMAIL'
            }
        )

    def test_user_post_signup_phone_number_exists_validation(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'kimapple',
                'email'         : 'applee99@gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-9999-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'ALREADY_EXISTS_PHONE_NUMBER'
            }
        )

    def test_user_post_signup_key_error(self):
        user = {
                'korean_name'   : '김애플',
                'email'         : 'applee24@gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1234-1234',
                'gender'        : 'male',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'KEY_ERROR'
            }
        )

    def test_user_post_signup_gender_does_not_exist_error(self):
        user = {
                'korean_name'   : '김애플',
                'english_name'  : 'pineapple',
                'email'         : 'poewee@gmail.com',
                'password'      : '123456aA!',
                'date_of_birth' : '1992-04-24',
                'phone_number'  : '010-1002-1234',
                'gender'        : 'mmal',
                'country'       : '대한민국'
                }
        response = self.client.post('/user/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'DOES_NOT_EXIST_GENDER'
            }
        )

    def test_user_post_signin_success(self):
        user = {
                'email'    : 'applee24@gmail.com',
                'password' : '123456aA!'
                }

        response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'access_token' : response.json()['access_token']
            }
        )
    def test_user_post_signin_emailformat_validation(self):
        user = {
                'email'    : 'applee24@gmailcom',
                'password' : '123456aA!'
                }

        response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'INCORRECT_EMAIL_FORMAT'
            }
        )

    def test_user_post_signin_user_email_validation(self):
        user = {
                'email'    : 'muntroo@gmail.com',
                'password' : '122256aA!'
                }

        response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
                {
                    'MESSAGE' : 'DOES_NOT_EXIST_USER'
                }
        )

    def test_user_post_signin_user_password_validation(self):
        user = {
                'email'    : 'applee24@gmail.com',
                'password' : '123444aA!'
                }

        response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_user_post_signin_user_information_validation(self):
        user = {
                'email'    : 'muntrock@gmail.com',
                'password' : '123444aA!'
                }

        response = self.client.post('/user/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'DOES_NOT_EXIST_USER'
            }
        )

    @patch('user.views.requests')
    def test_user_post_kakao_signin_success(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {'kakao_account': {
                            'profile'  : {'nickname': '문타리'},
                            'email'    : 'applee24@gmail.com',
                            }
                        }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        header             = {'HTTP_Authorization' : 'access_token'}
        response           = self.client.post('/user/signin/kakao', content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_user_post_kakao_signin_not_exist_user(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {'kakao_account': {
                            'profile'  : {'nickname': '문타리'},
                            'email'    : 'AAAAAAA@gmail.com',
                            }
                        }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        header             = {'HTTP_Authorization' : 'access_token'}
        response           = self.client.post('/user/signin/kakao', content_type='application/json', **header)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : 'NOT_EXIST_USER',
                'EMAIL'   : 'AAAAAAA@gmail.com',
                'NAME'    : '문타리'
            }
        )

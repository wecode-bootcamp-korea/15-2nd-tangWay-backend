import unittest, json, bcrypt, jwt

from datetime      import datetime, timedelta
from django.test   import TestCase, Client

from my_settings   import SECRET_KEY, JWT_ALGORITHM
from user.models   import Gender, Country, User
from flight.models import Service, Country, Airport, Airplane, PathType, FlightImage, CalenderPrice, Price, Calender, Flight

class ServiceBundleTest(TestCase):
    def setUp(self):
        Service.objects.create(
                name      = '면세품',
                image_url = 'https://www.flaticon.com/svg/static/icons/svg/869/869104.svg'
                )

    def tearDown(self):
        Service.objects.all().delete()

    def test_flight_servicebundle_view_success(self):
        client   = Client()
        response = client.get('/flight/service', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'SERVICE' : [
                    {
                        'name'  : '면세품',
                        'image' : 'https://www.flaticon.com/svg/static/icons/svg/869/869104.svg'
                        }
                    ]
            }
        )

class FlightImageTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        Country.objects.create(
                name = '대한민국'
                )

        Airport.objects.create(
                country_id   = 1,
                korean_name  = '서울/김포',
                english_name = 'GIM'
                )

        Airport.objects.create(
                country_id   = 1,
                korean_name  = '제주',
                english_name = 'JEJ'
                )

        Airplane.objects.create(
                name = 'TW777'
                )

        Airplane.objects.create(
                name = 'TW281'
                )

        PathType.objects.create(
                name = '직항'
                )

        FlightImage.objects.create(
                image_url = 'https://images.unsplash.com/photo-1607727536244-b3ab855fb209?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
                )

        Price.objects.create(
                price = '10000.00'
                )

        Calender.objects.create(
                date    = '2021-01-10',
                day     = '월',
                premium = 20
                )

        CalenderPrice.objects.create(
                price_id    = 1,
                calender_id = 1
                )

        Flight.objects.create(
                depart_time        = '2021-01-10 20:00',
                arrive_time        = '2021-01-10 22:30',
                depart_date        = '2021-01-10',
                arrive_date        = '2021-01-14',
                adult              = 1,
                child              = 1,
                airplane_arrive_id = 1,
                airplane_depart_id = 2,
                airport_arrive_id  = 1,
                airport_depart_id  = 2,
                calender_price_id  = 1,
                image_id           = 1,
                path_type_id       = 1
                )

    def teadDown(self):
        Country.objects.all().delete()
        Airplane.objects.all().delete()
        Airport.objects.all().delete()
        PathType.objects.all().delete()
        Price.objects.all().delete()
        Calender.objects.all().delete()
        CalenderPrice.objects.all().delete()
        FlightImage.objects.all().delete()
        Flight.objects.all.delete()

    def test_get_flight_flight_image_view_spread_success(self):
        client   = Client()
        response = client.get('/flight/flight_image', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {'FLIGHT' : [
                    {
                        'arrive': '서울/김포',
                        'date'  : '2021-01-10T20:00:00Z',
                        'depart': '제주',
                        'id'    : 1,
                        'image' : 'https://images.unsplash.com/photo-1607727536244-b3ab855fb209?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
                        'price' : '10000.00'
                        }
                    ]
                    }
                )

class PassengerInformationTest(TestCase):
    def setUp(self):
        self.client     = Client()
        self.maxDiff    = None
        self.gender     = Gender.objects.create(name='male')
        self.country    = Country.objects.create(name='대한민국')

        hashed_password = bcrypt.hashpw('123456aA!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
                 id            = 1,
                 korean_name   = '문타리',
                 english_name  = 'munshee',
                 email         = 'munshee@naver.com',
                 password      = hashed_password,
                 date_of_birth = '19920424',
                 phone_number  = '01010101234',
                 gender_id     = self.gender.id,
                 country_id    = self.country.id
                 )

    def tearDown(self):
        Gender.objects.all().delete()
        Country.objects.all().delete()
        User.objects.all().delete()

    def test_flight_get_passenger_information_success(self):
        signin_user     = {
                'email'    : 'munshee@naver.com',
                'password' : '123456aA!'
                }
        signin_response = self.client.post('/user/signin', json.dumps(signin_user), content_type='application/json')

        header          = {'HTTP_Authorization' : signin_response.json()['access_token']}
        response        = self.client.get('/flight/passenger', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                {
                    'USER_INFORMATION'  : {
                        'country'       : '대한민국',
                        'date_of_birth' : '19920424',
                        'email'         : 'munshee@naver.com',
                        'gender'        : 'male',
                        'name'          : '문타리',
                        'phone_number'  : '01010101234'
                        }
                })

    def test_flight_get_passenger_information_not_exist_access_token_error(self):
        header   = {'HTTP_Authorization' : None}
        response = self.client.get('/flight/passenger', content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'INCORRECT_USER_INFORMATION'
                })

    def test_flight_get_passenger_information_jwt_decode_error(self):
        signin_user     = {
                'email'    : 'munshee@naver.com',
                'password' : '123456aA!'
                }
        signin_response = self.client.post('/user/signin', json.dumps(signin_user), content_type='application/json')

        header          = {'HTTP_Authorization' : signin_response.json()['access_token'] + 'raise_jwt_decode_error'}
        response        = self.client.get('/flight/passenger', content_type='application/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'INCORRECT_USER_INFORMATION'
                })

    def test_flight_get_passenger_information_user_does_not_exist_error(self):
        signin_user     = {
                'email'    : 'munshee@naver.com',
                'password' : '123456aA!'
                }
        signin_response = self.client.post('/user/signin', json.dumps(signin_user), content_type='application/json')

        header          = {'HTTP_Authorization' : signin_response.json()['access_token']}
        self.tearDown()
        response        = self.client.get('/flight/passenger', content_type='application/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'INCORRECT_USER_INFORMATION'
                })

    def test_flight_get_passenger_jwt_expried_error(self):
        payload  = {'user-id' : 1, 'exp' : datetime.now() -timedelta(hours=10)}
        token    = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

        header   = {'HTTP_Authorization' : token}
        response = self.client.get('/flight/passenger', content_type='application/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE' : 'EXPIRED_TOKEN'
                })

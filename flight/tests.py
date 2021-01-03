import unittest, json
from django.test   import TestCase, Client
from flight.models import Service

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



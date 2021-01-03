import json

from django.views  import View
from django.http   import JsonResponse

from flight.models import Service, Flight

class ServiceBundleView(View):
    def get(self, request):
        services = Service.objects.all()
        service  = [
                {
                    'name' : service.name,
                    'image' : service.image_url
                } for service in services]

        return JsonResponse({'SERVICE' : service}, status=200)

class FlightImageView(View):
    def get(self, request):
        flights = Flight.objects.select_related('airport_depart', 'airport_arrive', 'image', 'calender_price').all()
        flight  = [
                {
                    'id'     : flight.id,
                    'date'   : flight.depart_time,
                    'price'  : flight.calender_price.price.price,
                    'depart' : flight.airport_depart.korean_name,
                    'arrive' : flight.airport_arrive.korean_name,
                    'image'  : flight.image.image_url
                } for flight in flights]
        return JsonResponse({'FLIGHT' : flight}, status=200)

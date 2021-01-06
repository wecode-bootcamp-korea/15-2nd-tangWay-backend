import json, requests

from django.views  import View
from django.http   import JsonResponse

from user.models   import User, Country
from user.utils    import SigninConfirm 
from flight.models import Service, Flight, Airport

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

class PassengerInformationView(View):
    @SigninConfirm
    def get(self, request):
        user    = User.objects.select_related('gender', 'country').get(id=request.user.id)
        user_infomation = {
                'country'       : user.country.name,
                'date_of_birth' : user.date_of_birth,
                'email'         : user.email,
                'gender'        : user.gender.name,
                'name'          : user.korean_name,
                'phone_number'  : user.phone_number
                }
        
        return JsonResponse({'USER_INFORMATION' : user_infomation}, status=200)

class MainFlightView(View):
    def get(self, request, country_id):
        main_flights = Airport.objects.filter(country_id=country_id)
        
        if main_flights:
            country_airports = [
                    {
                        'id'           :  flight.id,
                        'korean_name'  : flight.korean_name,
                        'english_name' : flight.english_name
                    } for flight in main_flights]
            return JsonResponse({'country_airport' : country_airports}, status=200)
        return JsonResponse({'MESSAGE' : 'NOT_EXIST_COUNTRY'}, status=401)

class MainCountryView(View):
    def get(self, request):
        countrys = Country.objects.prefetch_related('airport_set').all()
        country  = [{
                    'id'       : country.id,
                    'name'     : country.name,
                    'airports' : [
                        {
                        'korean_name'  : airport.korean_name,
                        'english_name' : airport.english_name
                        } for airport in country.airport_set.all()]
                    } for country in countrys]

        return JsonResponse({'countrys' : country}, status=200)

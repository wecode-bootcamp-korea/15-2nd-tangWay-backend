import json, requests

from django.views  import View
from django.http   import JsonResponse

from user.models   import User
from user.utils    import SigninConfirm 
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

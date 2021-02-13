import json, requests
from django.views     import View
from django.http      import JsonResponse 
from django.db.models import Q
from user.models      import User, Country
from user.utils       import SigninConfirm 
from flight.models    import Service, Flight, Airport, Airplane, PathType, Calender, Price, CalenderPrice

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


#구간1
class Section1View(View):
    def get(self,request):

        query          = Q()
        airport_arrive = request.GET.get('airport_arrive')
        airport_depart = request.GET.get('airport_depart')        
        arrive_date    = request.GET.get('arrive_date')
        depart_date    = request.GET.get('depart_date')
        adult          = request.GET.get('adult')
        child          = request.GET.get('child')

        if airport_arrive:
            query &= Q(airport_arrive = airport_arrive)

        if airport_depart:
            query &= Q(airport_depart = airport_depart)

        if depart_date:
            query &= Q(depart_date = depart_date)

        if arrive_date:
            query &= Q(arrive_date = arrive_date)

        if adult:
            query &= Q(adult = int(adult))

        if child:
            query &= Q(child = int(child))
        
        flights = Flight.objects.select_related(
            'path_type',
            'airplane_arrive',
            'airplane_depart',
            'airport_depart',
            'airport_arrive'
        ).filter(query)
        
        airports = Flight.objects.select_related(
            'path_type',
            'airplane_arrive',
            'airplane_depart', 
            'airport_arrive', 
            'airport_depart'
        ).filter(query)
  
        section1_data =[{

            'data' :[{
                'id'                  : flight.id,
                'path_type'           : flight.path_type.name,
                'airplane_name'       : flight.airplane_depart.name,
                'depart_time'         : flight.depart_time.strftime('%H : %M'),
                'arrive_time'         : flight.arrive_time.strftime('%H : %M'),
                'depart_english_name' : flight.airport_depart.english_name,
                'arrive_english_name' : flight.airport_arrive.english_name,
                'price'               : int(flight.calender_price.price.price)
                }for flight in flights],

            'airport_korean_depart' : flight.airport_depart.korean_name,
            'depart_english_name'   : flight.airport_depart.english_name,
            'airport_korean_arrive' : flight.airport_arrive.korean_name,            
            'arrive_english_name'   : flight.airport_arrive.english_name,
            'depart_date'           : flight.depart_date,
            'arrive_date'           : flight.arrive_date
            }for flight in airports]
        
        return JsonResponse({'section1_data': section1_data}, status=200)

#구간2
class Section2View(View):
    def get(self,request):

        query          = Q()
        airport_arrive = request.GET.get('airport_arrive')
        airport_depart = request.GET.get('airport_depart')        
        arrive_date    = request.GET.get('arrive_date')
        depart_date    = request.GET.get('depart_date')
        adult          = request.GET.get('adult')
        child          = request.GET.get('child')
        
        if airport_arrive:
            query &= Q(airport_arrive = airport_arrive)

        if airport_depart:
            query &= Q(airport_depart = airport_depart)

        if depart_date:
            query &= Q(depart_date = depart_date)

        if arrive_date:
            query &= Q(arrive_date = arrive_date)

        if adult:
            query &= Q(adult = int(adult))

        if child:
            query &= Q(child = int(child))
        
        flights = Flight.objects.select_related(
            'path_type',
            'airplane_arrive',
            'airplane_depart',
            'airport_depart',
            'airport_arrive'
        ).filter(query)
        
        airports = Flight.objects.select_related(
            'path_type',
            'airplane_arrive',
            'airplane_depart', 
            'airport_arrive', 
            'airport_depart'
        ).filter(query)
  
        section2_data =[{
  
            'data' : [{
                'id'                  : flight.id,
                'path_type'           : flight.path_type.name,
                'airplane_name'       : flight.airplane_depart.name,
                'depart_time'         : flight.depart_time.strftime('%H : %M'),
                'arrive_time'         : flight.arrive_time.strftime('%H : %M'),
                'depart_english_name' : flight.airport_depart.english_name,
                'arrive_english_name' : flight.airport_arrive.english_name,
                'price'               : int(flight.calender_price.price.price)
                }for flight in flights],

            'airport_korean_depart' : flight.airport_depart.korean_name,
            'depart_english_name'   : flight.airport_depart.english_name,
            'airport_korean_arrive' : flight.airport_arrive.korean_name,            
            'arrive_english_name'   : flight.airport_arrive.english_name,
            'depart_date'           : flight.depart_date,
            'arrive_date'           : flight.arrive_date
            }for flight in airports]        
  
        return JsonResponse({'section2_data': section2_data}, status=200)


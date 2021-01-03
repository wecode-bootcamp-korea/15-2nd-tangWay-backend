import json

from django.views  import View
from django.http   import JsonResponse

from flight.models import Service

class ServiceBundleView(View):
    def get(self, request):
        services = Service.objects.all()
        service  = [
                {
                    'name' : service.name,
                    'image' : service.image_url
                } for service in services]

        return JsonResponse({'SERVICE' : service}, status=200)

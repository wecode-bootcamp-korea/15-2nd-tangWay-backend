from django.urls  import path
from flight.views import ServiceBundleView, FlightImageView

urlpatterns = [
        path('/service',ServiceBundleView.as_view()), 
        path('/flight_image', FlightImageView.as_view()),
]

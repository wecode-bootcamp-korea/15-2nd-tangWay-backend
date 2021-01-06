from django.urls  import path
from flight.views import ServiceBundleView, FlightImageView, MainFlightView, MainCountryView, PassengerInformationView

urlpatterns = [
        path('/service',ServiceBundleView.as_view()), 
        path('/flight_image', FlightImageView.as_view()),
        path('/passenger', PassengerInformationView.as_view()),
        path('/<int:country_id>', MainFlightView.as_view()),
        path('/country' , MainCountryView.as_view())
]

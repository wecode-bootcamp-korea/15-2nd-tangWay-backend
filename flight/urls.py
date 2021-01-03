from django.urls  import path
from flight.views import ServiceBundleView, PassengerInformationView

urlpatterns = [
        path('/service',ServiceBundleView.as_view()), 
        path('/passenger', PassengerInformationView.as_view()),
]

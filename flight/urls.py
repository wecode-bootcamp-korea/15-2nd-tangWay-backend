from django.urls  import path
from flight.views import ServiceBundleView

urlpatterns = [
        path('/service',ServiceBundleView.as_view()), 
]

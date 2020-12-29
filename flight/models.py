from django.db   import models
from user.models import User, Country, Gender

class Airport(models.Model):
    korean_name  = models.CharField(max_length=16)
    english_name = models.CharField(max_length=32)
    country      = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'airports'

    def __str__(self):
        return self.korean_name

class Airplane(models.Model):
    name = models.CharField(max_length=8)

    class Meta:
        db_table = 'ariplanes'

class PathType(models.Model):
    name = models.CharField(max_length=8)

    class Meta:
        db_table = 'path_types'

class Calender(models.Model):
    date    = models.DateField()
    day     = models.CharField(max_length=8)
    premium = models.IntegerField(null=True)

    class Meta:
        db_table = 'calenders'

class Price(models.Model):
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    change_amounts = models.ManyToManyField(Calender, through='CalenderPrice')

    class Meta:
        db_table = 'prices'

class PassengerInformation(models.Model):
    english_name  = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    gender        = models.ForeignKey(Gender, on_delete=models.CASCADE)
    country       = models.ForeignKey(Country, on_delete=models.CASCADE)
    boardings     = models.ManyToManyField(User, through='UserPassengerInformation')

    class Meta:
        db_table = 'passenger_informations'

class FlightImage(models.Model):
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'flight_images'

class Service(models.Model):
    name      = models.CharField(max_length=16)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'services'

class UserPassengerInformation(models.Model):
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_information = models.ForeignKey(PassengerInformation, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_passenger_informations'

class CalenderPrice(models.Model):
    price    = models.ForeignKey(Price, on_delete=models.CASCADE)
    calender = models.ForeignKey(Calender, on_delete=models.CASCADE)

    class Meta:
        db_table = 'calender_pirces'

class Flight(models.Model):
    depart_time     = models.DateTimeField()
    arrive_time     = models.DateTimeField()
    depart_date     = models.DateField()
    arrive_date     = models.DateField()
    adult           = models.IntegerField()
    child           = models.IntegerField()
    airport_depart  = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='depart')
    airport_arrive  = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrive')
    airplane_depart = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='number_depart')
    airplane_arrive = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='number_arrive')
    path_type       = models.ForeignKey(PathType, on_delete=models.CASCADE)
    image           = models.ForeignKey(FlightImage, on_delete=models.CASCADE)
    calender_price  = models.ForeignKey(CalenderPrice, on_delete=models.CASCADE)

    class Meta:
        db_table= 'flights'


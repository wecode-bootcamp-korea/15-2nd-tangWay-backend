from django.db import models

class Gender(models.Model):
    name = models.CharField(max_length=8)

    class Meta:
        db_table = 'genders'

class Country(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = 'countrys'

class User(models.Model):
    korean_name   = models.CharField(max_length=32)
    english_name  = models.CharField(max_length=32)
    password      = models.CharField(max_length=128)
    email         = models.EmailField(max_length=64)
    phone_number  = models.CharField(max_length=16)
    date_of_birth = models.CharField(max_length=16)
    gender        = models.ForeignKey(Gender, on_delete=models.CASCADE)
    country       = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'


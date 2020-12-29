from django.db     import models
from user.models   import User
from flight.models import Flight

class Status(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = 'statuses'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'payment_methods'

class Payment(models.Model):
    card_number    = models.IntegerField()
    cvv            = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    class Meta:
        db_table = 'payments'

class Reservation(models.Model):
    create_at          = models.DateTimeField(auto_now_add=True)
    update_at          = models.DateTimeField(auto_now=True)
    reservation_number = models.TextField()
    user               = models.ForeignKey(User, on_delete=models.CASCADE)
    flight             = models.ForeignKey(Flight, on_delete=models.CASCADE)
    status             = models.ForeignKey(Status, on_delete=models.CASCADE)
    payment            = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'


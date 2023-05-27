from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class packages(models.Model):
    pack_name = models.CharField(max_length=100)
    pack_duration = models.CharField(max_length=100)
    pack_price = models.IntegerField() 
    pack_details = models.TextField()
    day_pickup = models.CharField(max_length=100)

    def __str__(self):
        return self.pack_name
    
class user_member(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    pack = models.ForeignKey(packages, on_delete=models.CASCADE)
    addr = models.CharField(max_length = 150)
    place = models.CharField(max_length = 50)
    pin_code = models.IntegerField()
    phone = models.IntegerField()

class delivery_status(models.Model):
    status = models.CharField(max_length=10)
    ui_text = models.CharField(max_length=100)

class history(models.Model):
    user_details = models.ForeignKey(user_member, on_delete=models.CASCADE)
    choice = models.ForeignKey(delivery_status, on_delete=models.CASCADE)
    day_picked = models.DateTimeField()

    def __str__(self):
        return f"{self.user_details.addr}"

class picker_schedule(models.Model):
    emp_name = models.ForeignKey(User, on_delete=models.CASCADE)
    pick_place =  models.ForeignKey(history, on_delete=models.CASCADE)
    

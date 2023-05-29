from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)  
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=4)
    email_status = models.CharField(max_length=100, default='Inactive')

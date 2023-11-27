# address/models.py
from django.db import models
from users.models import User

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"




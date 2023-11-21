from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username



class Products(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

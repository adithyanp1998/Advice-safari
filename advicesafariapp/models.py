import uuid
from django.db import models
from django.contrib.auth import get_user_model 
# from django.views.generic import ListView
# from .models import Product
# Create your models here.
# models.py
User = get_user_model()

class PasswordReset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_when = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"Password reset for {self.user.username} at {self.created_when}"

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    phonenumber = models.BigIntegerField()  # Change to BigIntegerField
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.title
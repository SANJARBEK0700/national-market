from django.contrib.auth.models import AbstractUser
from django.db import models
import random



class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)


    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.username
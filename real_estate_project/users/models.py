from django.db import models
from django.contrib.auth.models import User

from listings.models import Property


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wishlist = models.ManyToManyField(Property, related_name="wishlisted_by", blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'



from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    # items of listings
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    price = models.IntegerField()
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    image = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.title}\n{self.description}"
    pass


class Bid(models.Model):
    # buyer =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    # bid = models.IntegerField(max_length = price)
    pass

class Comment(models.Model):
    pass
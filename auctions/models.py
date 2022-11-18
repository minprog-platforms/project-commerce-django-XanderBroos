from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    # items of listings
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    price = models.IntegerField()
    min_bid = models.IntegerField()
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    image = models.CharField(max_length=1000)
    current_bid = models.IntegerField()
    bidder = models.CharField(max_length=1000)
    

    def __str__(self) -> str:
        return f"{self.title}"
    pass


class Bid(models.Model):
    # user =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    
    # title_item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="title")
    # buyer =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    # bid = models.IntegerField(min_length="min_bid", max_length="price") 
    # current_bid = models.IntegerField()
    # def __str__(self) -> str:
    #     return f"{self.title}"
    pass


class Comment(models.Model):
    # commenter =models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    # comment =  models.CharField(max_length=1000)
    pass
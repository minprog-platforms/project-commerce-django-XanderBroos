from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    """
    Vereiste items voor een listing:
    title van de listing
    omschrijving van listing
    koopprijs van listing 
    minimum prijs om te bieden
    Moet kijken of listing nog active is 
    owner van de listing, verkoper dus
    Huidig hoogste bid van user

    Moet ook nog verbindingen gaan maken met de classes comments en bids
    """
    # items of listings
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    price = models.IntegerField()
    min_bid = models.IntegerField()
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    image = models.CharField(max_length=1000)
    current_bid = models.IntegerField()
    current_bidder = models.CharField(max_length=1000, default="Xander")
   

    def __str__(self) -> str:
        return f"{self.title}"
    pass


class Bid(models.Model):
    """
    Wordt alleen gebruikt in listing page.
    Heeft de items, zodat een user een bid kan plaatsen, en dat de class dan ook de gegevens heeft
    over wie heeft geboden, de user, en op welk item is geboden. 
    bid_user is de user die nu is ingelogd, en die blijft hetzelfde, ook als iemand anders is ingelogd
    title_item zorgt dat het bod op item, hetzelfde item is als de item van de huidige pagina

    """
    # bid_user =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True,  related_name="bid_user")
    title_item = models.CharField(max_length=1000)
    bid = models.IntegerField() 
    bid_user = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.bid_user}"
    pass


class Comment(models.Model):
    """
    Wordt alleen gebruikt wanneer je op de listing pagina bent.
    Heeft de items, zodat je een comment kan opslaan,  en van die comment weet wie
    die comment heeft geschreven, en bij welke item deze comment hoort
    comment_user is de user die is ingelogd tijdens het maken van de comment
    comment_title zorgt dat de comment alleen er staat bij de item van huidige pagina
    comment_tekst onthoudt alle tekst in comment
    """
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    comment_tekst =  models.CharField(max_length=1000)
    comment_title = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return f"{self.comment_tekst}"


    pass
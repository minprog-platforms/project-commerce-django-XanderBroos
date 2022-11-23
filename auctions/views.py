from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid , Comment


def index(request):
    entries = Listing.objects.filter(active=True)
    closed_entries = Listing.objects.filter(active=False)
    return render(request, "auctions/index.html", {
        "list": entries, "other_list":closed_entries
    })

def listing(request, name):
    try:
        item = Listing.objects.get(title=f"{name}")
    except Listing.DoesNotExist:
        item = None

    try:
        comment_list = Comment.objects.filter(comment_title=f"{name}")
    except Comment.DoesNotExist:
        comment_list = None



        
    if request.method == "GET":


        # if listing is gesloten en ingelogde user is user laatste bod

        accept=False
        if request.user == item.owner:
            accept = True
        con=True
        gewonnen="ge"
        if item.active:
            con=False
        else:
            haha = str(request.user)
            if haha == item.current_bidder:
                gewonnen="Gefeliciteerd, je hebt gewonnen"
            else:
                gewonnen="Helaas, je hebt dit item niet gewonnen"

        
        return render(request, "auctions/listing.html", {
            "item": item, "accept":accept, "comment":comment_list, "con":con, "test":gewonnen
        })
    else:
        # Zorg dat je een watchlist kan toevoegen 

        # check = False
        # watch = request.POST["watch"]
        # if watch == True:
        #     check = True
        
        # verkrijg juist bid item
        # bid_item = Listing.objects.get(title=f"{name}")
        try:
            bid = int(request.POST["bid"])
        except:
            bid = 0

        try:
            actief = request.POST["done"]
        except:
            actief = "Niet"

        try:
            comment = str(request.POST["comment"])
        except:
            comment = "None"

        

        if actief == "done":
            actief =False
        else:
            actief=True

        # !!!! moet uit Listing, moet in Bid class
        if bid > item.current_bid:
            # save new bid as current bid
            item.current_bid = bid
            # save current user
            name_bid = str(request.user)
            item.current_bidder = name_bid
            

            
            # save the whole item
            

        item.active=actief
        item.save()

        if comment != "None":
            comment_for = Comment(
                comment_user=request.user,
                comment_title=f"{name}",
                comment_tekst="placeholder"
            )
            comment_for.comment_tekst=comment
            comment_for.save()
            


        # Zorg dat je comment kan plaatsen
            # gebruik post comment
            # update lijst van alle comments in Comments class

        # Zorg dat je auction kan sluiten met button
            # als gesloten, scherm moet zeggen dat gewonnen
        
        # Redirect response and go back to homepage
        return HttpResponseRedirect(reverse(index))

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description =request.POST["desc"]
        bid =request.POST["bid"]
        url =request.POST["url"]
        min_bid = request.POST["min_bid"]
        user = request.user
        
        new_listing = Listing(
            title=title,
            description=description,
            price=bid,
            min_bid=min_bid,
            active=True,
            current_bid=min_bid,
            owner=user,
            image=url)

        new_listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, "auctions/create.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

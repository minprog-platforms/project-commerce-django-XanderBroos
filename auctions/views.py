from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    entries = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "list": entries
    })

def listing(request, name):
    try:
        item = Listing.objects.get(title=f"{name}")
    except Listing.DoesNotExist:
        item = None
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "item": item
        })
    else:
        # bid_item = Listing.objects.get(title=f"{name}")
        bid = int(request.POST["bid"])
        # user = request.user
        if bid > item.current_bid:
            item.current_bid = bid
            item.save()
        return HttpResponseRedirect(reverse(index))
        return render(request, "auctions/listing.html", {
            "item": item
        })

    pass


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

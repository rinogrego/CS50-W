from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

from datetime import date
from django.utils import timezone


def index(request):
    if request.method == "POST" and request.POST.get('title'):
        #form = ListingForm(request.POST, request.FILES)
        new_title = request.POST.get('title')
        new_image = request.FILES.get('image')
        new_category = request.POST.get('category')
        new_description = request.POST.get('description')
        new_price = request.POST.get('price')
        new_date_end = request.POST.get('date_end')

        a = Listing.objects.create(
            user = request.user, 
            title = new_title, 
            image = new_image,
            category = new_category, 
            description = new_description, 
            price = new_price, 
            date_end = new_date_end,
            status = True
        )
        a.save()
        
        listing_get = Listing.objects.get(title=new_title)
        if listing_get.date_end != "":
            if not listing_get.is_available:
                listing_get.status = False
                listing_get.save()
        
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.all(),
    })


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


def profile(request, nama):
    profile_data = User.objects.get(username=nama)
    return render(request, "auctions/profile.html", {
        "User": profile_data,
    })

def listing(request, namaBarang):
    if request.user.is_authenticated:
        user_balance = float(request.user.balance)
    else:
        user_balance = 0
    listing_data = Listing.objects.get(title=namaBarang)
    listing_data_watchlist = listing_data.watchlist.all()
    try:
        bid_data = listing_data.Bid_Data.latest('date_made')
    except:
        bid_data = False
    if str(request.user.username) == str(listing_data.user):
        owner_listing_status = True
    else:
        owner_listing_status = False
    if request.method == "POST":
        if request.POST.get('comment'):
            form = CommentListing(request.POST)
            if form.is_valid():
                content = request.POST.get('comment')
                a = ListingComment.objects.create(user=request.user, title=listing_data, comment=content)
                a.save()
        elif request.POST.get('price'):
            form = BiddingForm(request.POST)
            new_price = float(request.POST.get('price'))
            old_price = float(listing_data.price)
            if form.is_valid() and new_price > old_price and new_price <= user_balance:
                newbid = Bid.objects.create(user=request.user, title=listing_data, price=new_price)
                newbid.save()
                listing_data.price = new_price
                listing_data.save()
                request.user.balance = float(user_balance - new_price)
                request.user.save()
            elif form.is_valid() and new_price > old_price and new_price > user_balance:
                bidder = request.user.username
                bidForm = BiddingForm(initial={
                    "user": bidder,
                    "price": new_price,
                })
                message3 = "Your Bid Exceed Your Balance. \
                            Please Place a Proper Bid."
                return render(request, "auctions/bid.html", {
                    "barang": namaBarang,
                    "currentBid": old_price,
                    "bidForm": bidForm,
                    "message3": message3,
                    "bid_data": bid_data,
                    "owner_listing_status": owner_listing_status,
                })
            elif form.is_valid():
                bidder = request.user.username
                bidForm = BiddingForm(initial={
                    "user": bidder,
                    "price": old_price,
                })
                message = "Please submit a higher bid"
                message2 = False
                if user_balance < old_price:
                    message2 = "Your Balance Is Not Enough"
                return render(request, "auctions/bid.html", {
                    "barang": namaBarang,
                    "currentBid": old_price,
                    "bidForm": bidForm,
                    "message": message,
                    "message2": message2,
                    "bid_data": bid_data,
                    "owner_listing_status": owner_listing_status,
                })
        elif not request.POST.get('price') and not request.POST.get('comment'):
            listing_data.status = False
            listing_data.save()

    #listing_data = Listing.objects.filter(title=nama).order_by('id').first() # to prevent MultipleObjectsReturned Error.
    comment_data = listing_data.Listing_Comment.all()
    commentForm = False
    if request.user.is_authenticated:
        commentForm = CommentListing(initial={
            'user': request.user,
            'title': listing_data,
        })
    try:
        if str(request.user.username) == str(bid_data.user):
            bid_win_status = True
        else:
            bid_win_status = False
    except:
        bid_win_status = False

    return render(request, "auctions/listing.html", {
        "Listing": listing_data,
        "Comments": comment_data,
        "commentForm": commentForm,
        "bid_data": bid_data,
        "owner_listing_status": owner_listing_status,
        "bid_win_status": bid_win_status,
        "bid_availability": Listing.is_available,
        "listing_watchlist": listing_data_watchlist,
    })

def category(request):
    listing_data = Listing.objects.all()
    categorydict = []
    for category__ in listing_data:
        if category__.category not in categorydict:
            categorydict.append(category__.category)
    return render(request, "auctions/category.html", {
        "Categories": categorydict,
    })

def Category_Category(request, category_category):
    return render(request, "auctions/category_category.html", {
        "Category": category_category,
        "Listings": Listing.objects.all(),
    })

@login_required(login_url='login')
def watchlist(request, nama):
    try:
        watchlist_data = User.objects.get(username=nama).Watchlist.all()
        user_existence = True
    except User.DoesNotExist:
        watchlist_data = None
        user_existence = False
    return render(request, "auctions/watchlist.html", {
        "Watchlist": watchlist_data,
        "nama": nama,
        "user_existence": user_existence,
    })

@login_required(login_url='login')
def add_watchlist(request, namaBarang):
    if request.user.is_authenticated:
        nama = request.user.username
    user_watching = User.objects.get(username=nama)
    listing_watched = Listing.objects.get(title=namaBarang).watchlist.add(request.user)
    return HttpResponseRedirect(reverse('listing', args=[namaBarang]))

@login_required(login_url='login')
def remove_watchlist(request, namaBarang):
    if request.user.is_authenticated:
        nama = request.user.username
    user_watching = User.objects.get(username=nama)
    listing_watched = Listing.objects.get(title=namaBarang).watchlist.remove(request.user)
    return HttpResponseRedirect(reverse('listing', args=[namaBarang]))
      
@login_required(login_url='login')
def create_new_listing(request):
    form = ListingForm(initial={'category': ''})
    return render(request, "auctions/createalisting.html", {
        "form": form,
    })


@login_required(login_url='login')
def bid(request, namaBarang):
    user_balance = float(request.user.balance)
    if request.user.is_authenticated:
        bidder = request.user.username
    currentPrice = float(Listing.objects.get(title=namaBarang).price)
    bidForm = BiddingForm(initial={
        "user": bidder,
        "price": currentPrice,
    })
    message2 = False
    if user_balance < currentPrice:
        message2 = "Your Balance Is Not Enough"
    return render(request, "auctions/bid.html", {
        "barang": namaBarang,
        "currentBid": currentPrice,
        "bidForm": bidForm,
        "message2": message2,
    })
from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date, datetime


class User(AbstractUser):
    image = models.ImageField(blank=True, null=True, upload_to='media/profile/')
    balance = models.FloatField(default=0)
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    image = models.ImageField(max_length=255, blank=True, null=True, upload_to='media/listing/')
    category = models.CharField(max_length=32, null=True, blank=False, default="uncategorized")
    description = models.TextField(max_length=512, null=True, blank=True)
    price = models.FloatField(blank=False, null=True, default=0)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    date_bid = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    date_end = models.DateTimeField(null=True, blank=True)
    
    #date_now = datetime.strptime(date.today(), "%Y-%m-%d").date()
    date_now = models.DateTimeField(auto_now=True, editable=False)

    watchlist = models.ManyToManyField(User, blank=True, related_name="Watchlist")
    status = models.BooleanField(default=True, null=False, blank=False)

    """ I Don't Know What I am Doing """

    @property
    def is_available(self):
        try:
            return self.date_now <= self.date_end
        except:
            return True

    def __str__(self):
        return f"{self.title} ({self.user})" 

class ListingComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="Listing_Comment")
    title = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Listing_Comment")
    comment = models.TextField(max_length=1024, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user} has made a comment towards listing {self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bid_Data")
    title = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bid_Data")
    price = models.FloatField(blank=False, null=False, default=0)
    date_made = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.user} has made a bid for {self.title} for {self.price}"


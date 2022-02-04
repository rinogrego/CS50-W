from django.contrib import admin

# Register your models here.
from .models import *

class ListingAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "title", "category", "price", "status", "date_now", "date_end")
  filter_horizontal = ("watchlist", )

class UserAdmin(admin.ModelAdmin):
  list_display = ("id", "username", "image", "balance")


class ListingCommentAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "title", "comment", "date_posted")

class BidAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "title", "price", "date_made")
  


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingComment, ListingCommentAdmin)
admin.site.register(Bid, BidAdmin)
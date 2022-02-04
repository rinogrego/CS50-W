from django.contrib import admin

# Register your models here.
from .models import User, Post, Like

class UserAdmin(admin.ModelAdmin):
  filter_horizontal = ("follows", )

class PostAdmin(admin.ModelAdmin):
  list_display = ("id", "author", "content", "date")

class LikeAdmin(admin.ModelAdmin):
  list_display = ("user", "post", )

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)

from django.urls import path

from . import views

#app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:nama>", views.profile, name="profile"),
    path("<str:nama>/watchlist", views.watchlist, name="watchlist"),
    path("listing/category", views.category, name="category"),
    path("listing/create", views.create_new_listing, name="create_new_listing"),
    path("listing/<str:namaBarang>", views.listing, name="listing"),
    path("listing/<str:namaBarang>/add", views.add_watchlist, name="add_watchlist"),
    path("listing/<str:namaBarang>/remove", views.remove_watchlist, name="remove_watchlist"),
    path("listing/<str:namaBarang>/bid/", views.bid, name="bid"),
    path("listing/category/<str:category_category>", views.Category_Category, name="data_category"),
]

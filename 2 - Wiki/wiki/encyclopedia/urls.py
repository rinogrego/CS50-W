from django.urls import path

from . import views

"""
    self-note:
    Error in urlpatterns may break the entire server's work
    The order of path MATTERS
"""
urlpatterns = [
    path("index", views.index, name="index"),
    path("wiki/CreateNewEntry", views.createNewEntry, name="newEntry"),
    path("wiki/randomPage", views.randomPage, name="randomPage"),
    path("wiki/search", views.search, name="search"),
    path("wiki/<str:entry>", views.title, name="title"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
]

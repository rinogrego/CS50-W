
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:profile_name>", views.view_profile, name="view_profile"),
    path("profile/<str:profile_name>/follow", views.follow, name="follow"),
    path("gposts/<int:post_id>/like", views.like, name="like"),
    path("posts/<int:post_id>/edit", views.edit, name="edit"),

    # API routes
    path("posts", views.new_post, name="new_post"),
    path("posts/<str:posts_from>", views.posts, name="all_posts"),
    path("posts/<str:user>/likes", views.posts_user_like, name="posts_user_like"),
    path("profile/data/all", views.all_profiles, name="all_profiles"),
    path("profile/data/<str:profile_name>", views.profile, name="profile"),
    path('post/<int:post_id>', views.view_post, name="view_post"),
    # path("user/following", views.view_following_users, name="all_users"),
]

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *
import json


def index(request):
    
    posts = Post.objects.all()
    posts = posts.order_by("-date").all()
    
    """
    Dokumentasi Pribadi

        data_posts = [] # list for posts that the user like
        for x in range(0, len(posts)):
            try:
                # if user likes the post
                ====
                    # "request.user.id" AND "posts[x].likes.get(user=request.user).id" is the same, 
                    # but the former is used so that this try can throw an error, which will only happens
                    # if there is NO POST that liked by the currently logged in user.
                ====
                data_post = {
                    "is_liked": True,
                    "like_id": posts[x].likes.get(user=request.user).id,
                    "user": {
                        "id": posts[x].likes.get(user=request.user).user.id,
                        "username": posts[x].likes.get(user=request.user).user.username,
                    },
                    "post": {
                        "id": posts[x].likes.get(user=request.user).post.id,
                        "author": posts[x].likes.get(user=request.user).post.author.username,
                        "content": posts[x].likes.get(user=request.user).post.content,
                        "likes": posts[x].likes.count(),
                    },
                }
                data_posts.append(data_post)
            except:
                data_post = {
                    "is_liked": False,
                    "user": {
                        "id": request.user.id,
                        "username": request.user.username,
                    },
                    "post": {
                        "id": posts[x].id,
                        "author": posts[x].author.username,
                        "content": posts[x].content,
                        "likes": posts[x].likes.count(),
                    },
                }
                data_posts.append(data_post)
        # return JsonResponse([data_posts], safe=False)

        tests = posts[x].likes.filter(post=posts[x])
        test = [test.user.id for test in tests]
        if request.user.id in test:
            cek = {
                "user": request.user.username,
                "liked": True,
                "post": {
                    "id": posts[x].id,
                    "author": posts[x].author.username,
                    "content": posts[x].content,
                },
            }
        else:
            cek = {
                "user": request.user.username,
                "liked": False,
                "post": {
                    "id": posts[x].id,
                    "author": posts[x].author.username,
                    "content": posts[x].content,
                },
            }
        # return JsonResponse([cek], safe=False)

    """

    for post in posts:
        try:
            Like.objects.get(user=request.user, post=post)
            post.is_liked = True
        except:
            pass

    ## Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    first_half_page = int(page_number) - 3
    if first_half_page < 1:
        first_half_page = 1
    second_half_page = int(page_number) + 4

    paginator_length = []
    for i in range(first_half_page, second_half_page):
        paginator_length.append(i)

    paginator_max = paginator.num_pages + 1

    return render(request, "network/index.html", {
        # "Posts": posts,
        "Posts": page_obj,
        "Paginator_max": paginator_max,
        "Paginator_Length": paginator_length,
    })


def following(request):

    # get the people that followed by the user
    followed_people = User.objects.filter(followers=request.user)

    # get their posts
    posts = Post.objects.filter(author__in=followed_people)

    # arrange by latest post
    posts = posts.order_by("-date").all()

    # query like status
    for post in posts:
        try:
            Like.objects.get(user=request.user, post=post)
            post.is_liked = True
        except:
            pass

    ## Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    first_half_page = int(page_number) - 3
    if first_half_page < 1:
        first_half_page = 1
    second_half_page = int(page_number) + 4

    paginator_length = []
    for i in range(first_half_page, second_half_page):
        paginator_length.append(i)

    paginator_max = paginator.num_pages + 1

    return render(request, "network/index.html", {
        "Posts": page_obj,
        "Paginator_max": paginator_max,
        "Paginator_Length": paginator_length,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def view_profile(request, profile_name):

    # query profile data
    account = User.objects.get(username=profile_name)
    name = account.username
    email = account.email
    follower = account.followers.count()
    following = account.follows.count()

    try:
        # if the account is followed by the user
        account.followers.get(id=request.user.id)
        follow_status = True
    except:
        follow_status = False

    try:
        # if the account is following the user
        request.user.followers.get(id=account.id)
        followed_status = True
    except:
        followed_status = False

    # query posts authored by the viewed account
    posts = Post.objects.filter(author=account)
    posts = posts.order_by("-date").all()
    for post in posts:
        try:
            Like.objects.get(user=request.user, post=post)
            post.is_liked = True
        except:
            pass

    ## Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    first_half_page = int(page_number) - 3
    if first_half_page < 1:
        first_half_page = 1
    second_half_page = int(page_number) + 4

    paginator_length = []
    for i in range(first_half_page, second_half_page):
        paginator_length.append(i)

    paginator_max = paginator.num_pages + 1


    return render(request, "network/profile.html", {
        "name": name,
        "email": email,
        "follower": follower,
        "following": following,
        "follow_status": follow_status,
        "followed_status": followed_status,
        "Posts": page_obj,
        "Paginator_max": paginator_max,
        "Paginator_Length": paginator_length
    })


def follow(request, profile_name):

    account = User.objects.get(username=profile_name)

    try:
        # Check whether the user already follows the account or not
        User.objects.get(username=profile_name, followers=request.user)
        account.followers.remove(request.user)
    except:
        # if the user hasn't followed the account
        account.followers.add(request.user)

    return HttpResponseRedirect(reverse('view_profile', args=[profile_name]))


def like(request, post_id):

    post = Post.objects.get(id=post_id)

    # if user isn't logged in / anonymous
    if request.user.is_authenticated == False:
        return login_view(request)
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        # return JsonResponse({"message": "post disliked successfully!"})
    except Like.DoesNotExist: 
        like = Like(user=request.user, post=post)
        like.save()
        # return JsonResponse({"message": "post liked successfully!"})
    return HttpResponseRedirect(reverse('index'))


def edit(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        # Pengiriman Via Form Manual
        new_content = request.POST['content']
        post.content = new_content
        post.save()
        
        # I once tried to HardCoding this sh*t
        # return HttpResponse(request.body.decode('utf-8').strip('content=').replace('+', ' '))
        # test = request.body.decode('utf-8').strip('content=').replace('+', ' ')

        # try:
            # Pengiriman Via API/JavaScript
            # data = json.loads(request.body)
            # new_content = data.get('content')
            # post.content = new_content
            # post.save()
        # except:
        #     pass
        
        return JsonResponse({"message": "edit success"}, status=201)






    ###########################################
    #########      API FUNCTIONS       ########
    ##############               ##############
    ###########################################

@csrf_exempt
@login_required
def new_post(request):

    ##### W H Y  D I D  T H I S  F U N C T I O N  R U N  T W I C E ? ? ?
    ### First one succeeded because the post.save() below actually saved the new intended data, and the console spat out the {"message": "Post sent successfully."} Json response, meaning tis new_post function DID RUN SUCCESSFULLY once. 
    ### Second one is realized because somehow the error pointed to when request.body.decode('utf-8') contains only "", meaning the file already cleared, even though this function already ran once.
    ### I don't have a clue
    ### Maybe this can help, idk.
    ### https://stackoverflow.com/questions/45105767/django-view-getting-called-twice-double-get-request

    if request.method != "POST":
        return JsonResponse({"error": "Response harus berupa POST"}, status=400)

    try:
        data = json.loads(request.body)
        content = data.get("content")
    except: 
        # because this function (based on my observations) ran twice (idk why), i put this to go back to index.html
        posts = Post.objects.all()
        posts = posts.order_by("-date").all()
        return HttpResponseRedirect(reverse("index"))

    post = Post(
        author=request.user,
        content=content,
    )
    post.save()

    ### return JsonResponse(Post.objects.all()[0], safe=False) 
    ##### THINK I FOUND THE FKING PROBLEM ( I wrote this before I found the actual problem )
    ### PROBLEM: Looks like the fetch=>response in network.js take the value of html page from the above, or whatever get sent after this function finished running

    return JsonResponse({"message": "Post sent successfully."}, status=201)


@login_required
def posts(request, posts_from):

    posts = Post.objects.all()

    # query all posts
    if posts_from == "all":
        posts = Post.objects.all()

    # query posts from user's following
    elif posts_from == "following":
        # get the people that followed by the user
        followed_people = User.objects.filter(followers=request.user)
        # get their posts
        posts = Post.objects.filter(author__in=followed_people)
    else:
        return posts_user(request, posts_from)
        # return JsonResponse({"error": "please put in the correct url"}, status=400)

    posts = posts.order_by("-date").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


def posts_user(request, user):

    posts = Post.objects.filter(author__username=user)
    posts = posts.order_by("-date").all()
    posts = [post.serialize() for post in posts]

    # check the url
    if posts == []:
        return JsonResponse({"error": "wrong url or username to look at, or the user haven't made any post yet."}, safe=False)

    return JsonResponse(posts, safe=False)


def posts_user_like(request, user):

    posts = Post.objects.filter(likes__user__username=user)
    posts = posts.order_by("-date").all()
    posts = [post.serialize() for post in posts]

    return JsonResponse(posts, safe=False)


def view_post(request, post_id):

    post = Post.objects.get(id=post_id)

    return JsonResponse(post.serialize())


def all_profiles(request):

    accounts_data = User.objects.all()

    return JsonResponse([account_data.serialize() for account_data in accounts_data], safe=False)


def profile(request, profile_name):

    account_data = User.objects.get(username=profile_name)

    return JsonResponse([account_data.serialize()], safe=False)

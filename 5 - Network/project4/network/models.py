from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # make the username unique
    follows = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "number_of_following": self.follows.count(),
            "following": [account_followed.username for account_followed in self.follows.all()],
            "number_of_followers": self.followers.count(),
            "followers": [follower.username for follower in self.followers.all()],
            "number_of_posts": self.posts.count(),
            "posts": [{
                "id": post.id, 
                "author": post.author.username, 
                "content": post.content, 
                "date": post.date,
                "likes": self.likes.count(),
                } for post in self.posts.all()],
            "number_of_liked_posts": self.likes.count(),
        }
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    
    def is_liked(self):
        return False  # this may change depending on whether the user like the post or not.

    # to throw into API
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "date": self.date.strftime("%b-%d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "likers": [liker.user.username for liker in  self.likes.all()],
        }

    def __str__(self):
        return f'from: {self.author} >> "{self.content}"'


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE, null=True)
    # user = models.ManyToManyField(User, related_name="likes")
    # post = models.ManyToManyField(Post, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post,
            "created": self.created.strftime("%b-%d %Y, %I:%M %p"),
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_like"),
        ]

    # def __str__(self):
    #     return f"{self.user} likes {self.post.content}"
    
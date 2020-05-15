from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('core.Tag')

    def __str__(self):
        return self.title


class PostTime(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    spend_time = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

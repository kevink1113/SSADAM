from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import datetime


# Create your models here.


class User(AbstractUser):
    """ Custom User Model """

    avatar = models.ImageField(upload_to="avatars", blank=True)
    bio = models.CharField(blank=True, max_length=50)
    birthdate = models.DateField(blank=True, null=True)
    is_soldier = models.BooleanField(default=False)
    mil_start = models.DateField(blank=True, null=True)
    mil_fin = models.DateField(blank=True, null=True)
    mil_address = models.CharField(blank=True, null=True, max_length=100)
    homepage = models.URLField(blank=True, null=True)
    github_id = models.CharField(max_length=30, blank=True, null=True)
    blog = models.URLField(blank=True, null=True)
    boj_id = models.CharField(max_length=30, blank=True, null=True)
    student_id = models.PositiveIntegerField(blank=True, null=True)
    is_real = models.BooleanField(default=True)
    phone = models.CharField(blank=True, null=True,  max_length=16)
    address = models.CharField(blank=True, null=True, max_length=100)

    # like_posts = models.ManyToManyField( "posts.Post", blank=True, related_name="like_posts")
    # like_comments = models.ManyToManyField("comments.Comment", blank=True, related_name='like_comments')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.pk})

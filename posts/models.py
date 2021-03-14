from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from core import models as core_models
from django.urls import reverse
from comments import models as comment_models


class Post(core_models.TimeStampModel):
    """ Review Model Definition """
    ANONYMOUS = "anon"
    NOTICE = "notice"
    FREE = "free"

    BOARD_CHOICES = [
        (NOTICE, "공지"),
        (FREE, "자유게시판"),
        (ANONYMOUS, "익명게시판"),
    ]

    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="user_post", on_delete=models.CASCADE
    )

    board = models.CharField(
        choices=BOARD_CHOICES, max_length=10, default=FREE
    )

    # like = models.PositiveIntegerField(default=0)
    # dislike = models.PositiveIntegerField(default=0)

    like_users = models.ManyToManyField("users.User", related_name='like_posts', blank=True)
    dislike_users = models.ManyToManyField("users.User", related_name='dislike_posts', blank=True)

    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def like_sum(self):
        return self.like_users.count() - self.dislike_users.count()
        # return self.like - self.dislike

    def view_click(self):
        self.view_count += 1
        self.save()

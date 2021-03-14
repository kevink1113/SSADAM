from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampModel):
    """ Review Model Definition """

    content = models.TextField()
    post = models.ForeignKey(
        "posts.Post", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey("users.User", related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} - {self.content}"

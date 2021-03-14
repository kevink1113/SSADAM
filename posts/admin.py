from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """ Post Admin Definition """
    list_filter = ("user", "board", )
    list_display = ("created", "__str__", "user", "board", "like_sum",)



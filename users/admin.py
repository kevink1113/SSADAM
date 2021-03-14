from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from . import models


# admin.py에서 Model을 가져오려면 register를 해야 한다.
# models.User를 CustomUser에 사용하고자 한다.
# == admin.site.register(models.User, CustomUserAdmin)


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "student_id",
                    "bio",
                    "birthdate",
                    "homepage",
                    "github_id",
                    "blog",
                    "boj_id",
                )
            },
        ),
        ("군대", {"fields": ("is_soldier", "mil_start", "mil_fin", "mil_address")}),
    )
    list_filter = ("is_soldier",) + UserAdmin.list_filter
    list_display = (
        "username",
        "first_name",
        "student_id",
        "is_soldier",
        "birthdate",
        "homepage",
        "boj_id",
        "github_id",
        "is_active",
        "is_staff",
    )

    # filter_horizontal = ("like_posts",)

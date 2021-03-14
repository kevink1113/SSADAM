from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("create/<int:pk>", views.new_comment, name="new_comment"),
    path("delete/<int:pk>", views.delete_comment, name="delete_comment"),
    # url(r'^posts/new/$', views.new_post, name='new_post'),
]

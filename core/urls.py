from django.urls import path
from users import views as user_views

app_name = "core"

urlpatterns = [
    path("", user_views.UserView, name="home"),
    path("about/", user_views.About, name="about")
]

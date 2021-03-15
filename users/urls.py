from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("<int:pk>", views.UserDetail, name="detail"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("update-profile", views.UpdateProfileView.as_view(), name="update"),
    path("update-password", views.UpdatePasswordView.as_view(), name="password"),
    path("rank", views.rank, name="rank"),
    path("delete", views.UserDelete, name="delete")
]

from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostList.as_view(), name="list"),
    path("<int:pk>", views.PostDetail.as_view(), name="detail"),

    path("anon/", views.AnonList.as_view(), name="anon"),
    path("notice/", views.NoticeList.as_view(), name="notice"),
    path("free/", views.FreeList.as_view(), name="free"),
    path("trending/", views.TrendingList.as_view(), name="trending"),

    path("search/", views.SearchView.as_view(), name="search"),
    path("like/<int:pk>/", views.LikePost, name="LikePost"),
    path("dislike/<int:pk>/", views.disLikePost, name="disLikePost"),
    path("new/", views.NewPost, name="new_post"),
    path("delete/<int:post_pk>/", views.delete_post, name="delete"),
    path("modify/<int:post_pk>/", views.modify_post, name="modify"),
    # url(r'^posts/new/$', views.new_post, name='new_post'),
]

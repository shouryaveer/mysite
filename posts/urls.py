from django.urls import path

from . import views


app_name = "posts"

urlpatterns = [
    # path('', views.PostListView.as_view(), name="posts-list"),
    path('create', views.PostCreateView.as_view(), name="post-create"),
    path('', views.PostListView.as_view(), name="posts-feed"),
]
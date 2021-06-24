from django.urls import path
from django.conf.urls import url
from . import views


app_name = "posts"

urlpatterns = [
    # path('', views.PostListView.as_view(), name="posts-list"),
    path('create', views.PostCreateView.as_view(), name="post-create"),
    path('', views.PostListView.as_view(), name="posts-feed"),
    path('<pk>', views.PostDetailView.as_view(), name="post-detail"),
    path('<pk>/update', views.PostUpdateView.as_view(), name="post-update"),
    path('<pk>/delete', views.PostDeleteView.as_view(), name="post-delete"),
]
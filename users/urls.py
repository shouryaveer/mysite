from django.http.response import HttpResponseRedirect
from django.urls import path

from . import views
from posts.views import PostListView
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path('signup', views.SignUpFormView.as_view(), name="signup"),
    path('login/', views.LoginFormView.as_view(), name="login"),
    path('', PostListView.as_view(), name="home"),
    path('logout', views.logout_view, name="logout"),
    path('profile', views.SelfUserProfileView.as_view(), name="profile"),
    path('user/<pk>/profile', views.UserProfileView.as_view(), name="user-profile"),
    path('profile/update', views.ProfileUpdateView.as_view(), name="profile-update"),
    path('search/', views.SearchView.as_view(), name="search-users"),
]

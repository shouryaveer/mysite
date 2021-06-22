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
]

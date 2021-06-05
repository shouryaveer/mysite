from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path('signup', views.SignUpFormView.as_view(), name="signup"),
    path('login', views.LoginFormView.as_view(), name="login"),
]

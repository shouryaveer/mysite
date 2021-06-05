from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate

from .forms import CustomUserCreationForm, LoginForm, SignUpForm
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()
# Create your views here.

class SignUpFormView(View):
    form_class = SignUpForm
    initial = {'key': 'value'}
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if authenticate(request, username=username, password=password) is not None:
                user = authenticate(request, username=username, password=password)
            else:
                try:
                    user = UserModel.objects.get(email=username)
                    username = user.username
                    if authenticate(request, username=username, password=password) is not None:
                        user = authenticate(request,username=username, password=password)
                    else:
                        return render(request, self.template_name, {'form': form, 'invalid_user': True})
                except:
                    return render(request, self.template_name, {'form': form, 'invalid_user': True})

            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
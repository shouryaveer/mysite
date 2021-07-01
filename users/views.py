from api.users.serializers import UserProfileSerializer
from users.models import UserProfile, UserFollower
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignUpForm, UserProfileForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from django.utils.decorators import method_decorator

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
            username = form.cleaned_data.get("username")
            messages.success(request, "Account created for {}".format(username))
            return redirect('/login')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'users/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.GET.get('next'):
            self.context['redirect_url'] = request.GET.get('next')

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if authenticate(request, username=username, password=password) is not None:
                user = authenticate(request, username=username, password=password)
            else:
                try:
                    user = UserModel.objects.get(username=username)
                    username = user.email
                    if authenticate(request, username=username, password=password) is not None:
                        user = authenticate(request,username=username, password=password)
                    else:
                        return render(request, self.template_name, {'form': form, 'invalid_user': True})
                except:
                    return render(request, self.template_name, {'form': form, 'invalid_user': True})

            login(request, user)
            if self.context.get('redirect_url'):
                return HttpResponseRedirect(self.context['redirect_url'])
            else:
                return HttpResponseRedirect('/posts')

        return render(request, self.template_name, {'form': form})

def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, "{} logged out successfully".format(username))
    return redirect('/login')

@method_decorator(login_required, name="dispatch")
class SelfUserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(View):
    template_name = 'users/profile-update.html'

    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # form.update_user(request)
            messages.success(request, "User Profile Updated")
            return redirect('/profile')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class UserProfileView(View):

    template_name = 'users/profile.html'

    def get_queryset(self, request, pk):
        try:
            user = UserModel.objects.get(id=pk)
            return user
        except:
            messages.error(request, "User not Found!")
            return redirect('posts:posts-feed')

    def get(self, request, pk):
        user = self.get_queryset(request, pk)
        try:
            if UserFollower.objects.get(user=user, follower=request.user.id):
                is_followed = True
        except:
            is_followed = False
        return render(request, self.template_name, {'user': user, 'is_followed': is_followed})



@method_decorator(login_required, name="dispatch")
class UserFollowView(View):

    template_name = 'users/profile.html'

    def get_queryset(self, request, pk):
        try:
            user = UserModel.objects.get(id=pk)
            return user
        except:
            messages.error(request, "User not Found!")
            return redirect('posts:posts-feed')

    def get(self, request, pk):
        user = self.get_queryset(request, pk)
        request_user = UserModel.objects.get(id=request.user.id)
        UserFollower.objects.create(user=user, follower=request_user)
        user.profile.followers_count += 1
        request_user.profile.following_count += 1
        user.profile.save()
        request_user.profile.save()
        messages.success(request, "User {} followed successfully.".format(user.username))
        return redirect('/profile')


@method_decorator(login_required, name="dispatch")
class UserUnfollowView(View):

    template_name = 'users/profile.html'

    def get_queryset(self, request, pk):
        try:
            user = UserModel.objects.get(id=pk)
            return user
        except:
            messages.error(request, "User not Found!")
            return redirect('posts:posts-feed')

    def get(self, request, pk):
        user = self.get_queryset(request, pk)
        request_user = UserModel.objects.get(id=request.user.id)
        try:
            follower_data = UserFollower.objects.get(user=user, follower=request_user)
            follower_data.delete()
        except:
            messages.error(request, "You can't unfollow users that you don't follow!")
            return redirect('/profile')
        user.profile.followers_count -= 1
        request_user.profile.following_count -= 1
        user.profile.save()
        request_user.profile.save()
        messages.success(request, "User {} unfollowed successfully.".format(user.username))
        return redirect('/profile')

@method_decorator(login_required, name="dispatch")
class SearchView(View):

    template_name = 'users/search_results.html'

    def get(self,request, *args, **kwargs):
        query = request.GET.get('q')
        if query is not None:
            lookup = Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            results = UserModel.objects.filter(lookup).distinct()

            return render(request, self.template_name, {'users': results})
        else:
            return render(request, self.template_name)

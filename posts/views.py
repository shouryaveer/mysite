from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy

# Create your views here.
class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ('title', 'content', 'photo',)
    success_url = reverse_lazy('posts:posts-feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        else:
            return render(request, self.template_name, {'posts': Post.objects.all().order_by('-date_posted')})
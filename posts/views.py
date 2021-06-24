from posts.forms import PostCreateForm
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages

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
    # context_object_name = 'posts'
    # ordering = ['-date_posted']
    
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        else:
            return render(request, self.template_name, {'posts': Post.objects.all().order_by('-date_posted')})

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = ('title', 'content', 'photo',)
    success_url = reverse_lazy('posts:posts-feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    template_name = 'posts/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts:posts-feed')


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
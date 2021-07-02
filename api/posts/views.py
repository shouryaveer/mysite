from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from .serializers import PostSerializer
from users.models import User, UserFollower
from posts.models import Post
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters


# Create your views here.
class PostCreateView(CreateAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        post = Post(user=user)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Post created successfully',
            'post_detail': serializer.data,
            }
        
        return Response(response, status=status_code)

class PostsListView(ListAPIView, ListModelMixin):

    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    search_fields = ['title', 'content',]
    filter_backends = (filters.SearchFilter,)


class PostUpdateView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.user_id != request.user.id:
                raise ValidationError("User cannot edit/update other users posts.")
            else:
                serializer = self.serializer_class(post, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                status_code = status.HTTP_200_OK
                serializer.data["status_code"] = status_code
                serializer.data["message"] = "Post Updated Successfully"
                return Response(serializer.data, status=status_code)

        except Exception as e:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                'success': 'false',
                'status code': status.HTTP_404_NOT_FOUND,
                'message': 'Post Not Found!',
                'error': str(e)
            }
            return Response(response, status=status_code)

class PostDeleteView(DestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_queryset(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except:
            raise ValidationError("Post not found.")

    def delete(self, request, post_id):

        post = self.get_queryset(post_id)
        if post and post.user_id == request.user.id:
            post.delete()
        else:
            raise ValidationError("User cannot delete other users posts.")
        
        status_code = status.HTTP_200_OK
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Post deleted successfully',
        }
        return Response(response, status=status_code)

class PostFeedView(ListAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_queryset(self, request_user_id):
        users_followings = UserFollower.objects.filter(follower=request_user_id)

        if users_followings.exists():
            users_list = list(users_followings.values_list('user', flat=True))
        else:
            users_list = []
        
        users_list.append(request_user_id)
        posts = Post.objects.filter(user_id__in=users_list).order_by('-date_posted')

        return posts

    def list(self, request):
        queryset = self.get_queryset(request.user.id)
        serializer = PostSerializer(queryset, many=True)
        status_code = status.HTTP_200_OK
        response = {
            'success' : 'True',
            'status code' : status_code,
            'posts': serializer.data,
        }
        return Response(response, status=status_code)
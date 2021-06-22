from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from .serializers import PostSerializer
from users.models import User
from posts.models import Post
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.
class PostCreateView(CreateAPIView):

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        user = User.objects.get(email=request.user)
        request.data["user"] = user.id
        serializer = self.serializer_class(data=request.data)
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

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response({'posts': serializer.data})


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
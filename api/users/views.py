from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer, UserSerializer, UserLoginSerializer, UserSignUpSerializer
from users.models import User, UserProfile, UserFollower
from django.contrib.auth import login
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.serializers import ValidationError
from rest_framework_jwt.settings import api_settings


class UserRegistrationView(CreateAPIView):

    serializer_class = UserSignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered successfully',
            }
        
        return Response(response, status=status_code)


class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'token' : serializer.data['token'],
            }
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response_data = Response(response,status=status.HTTP_200_OK)
            response_data.set_cookie(api_settings.JWT_AUTH_COOKIE,response['token'],expires=expiration,httponly=True)
            return response_data

        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserListView(ListAPIView, ListModelMixin):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user = User.objects.get(email=request.user)
            serializer = self.serializer_class(user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'data': serializer.data,
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class UserProfileUpdateView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserProfileSerializer

    def put(self, request):
        try:
            user = UserProfile.objects.get(user=request.user.id)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_code = status.HTTP_200_OK
            serializer.data["status_code"] = status_code
            serializer.data["message"] = "User Profile Updated Successfully"
            return Response(serializer.data, status=status_code)

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
            return Response(response, status=status_code)

class FollowView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserProfileSerializer

    def get_queryset(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except:
            raise ValidationError("User not found.")

    def get(self, request, user_id):

        user = self.get_queryset(user_id)
        request_user = self.get_queryset(request.user.id)
        if not UserFollower.objects.filter(user=user_id, follower=request.user.id).exists():

            UserFollower.objects.create(user=user, follower=request_user)
            user = UserProfile.objects.get(user=user_id)
            request_user = UserProfile.objects.get(user=request.user.id)
            user.followers_count += 1
            request_user.following_count += 1
            user.save()
            request_user.save()
            serializer = self.serializer_class(user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User has been followed successfully',
                }

        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'You are already following this user.',
            }

        return Response(response, status=status_code)

class UnFollowView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserProfileSerializer

    def get_queryset(self, user_id, request_id):
        try:
            follower_data = UserFollower.objects.get(user_id=user_id, follower_id=request_id)
            return follower_data
        except:
            raise ValidationError("You need to be a follower of the user to Unfollow.")

    def get(self, request, user_id):

        follower_data = self.get_queryset(user_id, request.user.id)
        follower_data.delete()

        user = UserProfile.objects.get(user=user_id)
        request_user = UserProfile.objects.get(user=request.user.id)
        user.followers_count -= 1
        request_user.following_count -= 1
        user.save()
        request_user.save()
        serializer = self.serializer_class(user)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code,
            'message': 'User has been unfollowed successfully',
            }
        
        return Response(response, status=status_code)
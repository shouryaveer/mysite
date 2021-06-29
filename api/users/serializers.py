from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import User, UserProfile
import re
from PIL import Image
from django.contrib.auth.password_validation import validate_password

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'User with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User does not exist'
            )
        
        return {'email':user.email, 'token': jwt_token}


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'age', 'bio', 'profile_pic', 'followers_count', 'following_count',)


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=False)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages["required"] = u"username field is required"
        self.fields["email"].error_messages["required"] = u"email field is required"
        self.fields["password"].error_messages["required"] = u"password field is required"

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile',)
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        try:
            password = validate_password(password=validated_data.get("password"))
        except Exception as e:
            raise ValidationError(e)
        if re.match('^[0-9]', username) or re.match('^\.', username):
            raise ValidationError("Username cannot start with a number or a period(.)")

        if re.findall('\s', username):
            raise ValidationError("spaces are not allowed in username.")

        user = User.objects.create_user(**validated_data)
        # UserProfile.objects.create(user=user)

        return user
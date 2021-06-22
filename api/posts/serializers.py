from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from posts.models import Post
import re
from PIL import Image

class PostSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        self.fields["title"].error_messages["required"] = u"title field is required"
        self.fields["content"].error_messages["required"] = u"content field is required"

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'photo', 'user', 'date_posted', 'likes_count', 'comments_count',)


    def create(self, validated_data):

        title = validated_data.get('title')
        if Post.objects.filter(title=title).exists():
            raise ValidationError("Post title already exists.")
            
        post = Post.objects.create(**validated_data)

        return post
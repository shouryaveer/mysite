from django.db import models
import uuid
from PIL import Image
from datetime import datetime
from users.models import User
from django.utils import timezone
from src.utils import hex_uuid

# Create your models here.

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=hex_uuid, editable=False)
    title = models.CharField(max_length=150)
    content = models.TextField()
    photo = models.ImageField(upload_to='post-photos/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes_count = models.PositiveBigIntegerField(verbose_name="Likes Count", default=0)
    comments_count = models.PositiveBigIntegerField(verbose_name="Comments Count", default=0)

    class Meta:
        db_table = "posts"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo and self.photo is not None:
            img = Image.open(self.photo.path)
            img.save(self.photo.path)
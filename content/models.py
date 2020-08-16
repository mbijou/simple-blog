from django.db import models
from post.models import Content


class Image(models.Model):
    image_file = models.ImageField(null=True, blank=True)
    content = models.OneToOneField(Content, null=False, blank=False, on_delete=models.CASCADE)

from django.forms import ModelForm
from django.forms import FileField, BooleanField

from blog.base_forms import BootstrapForm
from post.models import Post


class PostForm(BootstrapForm, ModelForm):
    class Meta:
        model = Post
        fields = ("title", "sub_title", "published", "author", "post_image")

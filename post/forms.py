from django import forms
from blog.base_forms import BootstrapForm
from post.models import Post, MultiLanguagePostManager
from django.utils.translation import gettext_lazy as _


class PostForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "sub_title", "published", "author", "post_image")


class PostImportForm(BootstrapForm, forms.Form):
    file = forms.FileField(label=_("Import File"))

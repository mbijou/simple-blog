from django.forms import ModelForm
from post.models import Content
from content.models import Image
from post.models import image_choice
from blog.base_forms import BootstrapForm


class ContentForm(BootstrapForm, ModelForm):
    class Meta:
        model = Content
        fields = ("content", "type", "sequence", )

    def save(self, commit=True, post=None):
        if post is not None:
            self.instance.post = post
        return super().save(commit=commit)


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ("image_file",)


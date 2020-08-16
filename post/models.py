from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post_image = models.ImageField(null=True, blank=True)
    slug_title = models.SlugField(max_length=200, null=True)

    def title_slugified(self):
        return slugify(self.title)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug_title = slugify(self.title)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)


default_choice = "PARAGRAPH"
image_choice = "IMAGE"

type_choices = ((default_choice, "Paragraph"), ("SUBTITLE", "Subtitle"), (image_choice, "Image"),
                ("BLOCKQUOTE", "Blockquote"),)


class Content(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    content = models.TextField()
    sequence = models.IntegerField()
    type = models.CharField(null=False, blank=False, choices=type_choices, default=default_choice, max_length=200)

    def get_image(self):
        return getattr(self, "image", None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        contents_count = self.post.content_set.count()

        content_created = self.pk is None and self.post and contents_count > 0
        first_content_created = self.pk is None and contents_count == 0

        if content_created is True:
            actual_contents = self.post.content_set.order_by("sequence")
            if actual_contents.count() == 0:
                self.sequence = 1
            elif actual_contents.count() > 0:
                self.sequence = actual_contents.last().sequence + 1
        elif first_content_created is True:
            self.sequence = 0
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

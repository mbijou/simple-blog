from django.db import models
from django.db.models import F
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import translation
User = get_user_model()


class LocalLanguagePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(language_code=translation.get_language())


class MultiLanguagePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post_image = models.ImageField(null=True, blank=True)
    slug_title = models.SlugField(max_length=200, null=True, unique=True)
    language_code = models.CharField(null=False, blank=False, default=translation.get_language(), max_length=200)
    language_group = models.ForeignKey("post.LanguageGroup", null=True, on_delete=models.SET_NULL)

    objects = MultiLanguagePostManager()

    objects_from_all_languages = MultiLanguagePostManager()

    objects_from_local_language = LocalLanguagePostManager()

    def title_slugified(self):
        return slugify(self.title)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.language_code = translation.get_language()

        self.slug_title = slugify(self.title)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)


class LanguageGroup(models.Model):
    pass


default_choice = "PARAGRAPH"
image_choice = "IMAGE"

type_choices = ((default_choice, "Paragraph"), ("SUBTITLE", "Subtitle"), (image_choice, "Image"),
                ("BLOCKQUOTE", "Blockquote"), ("CODE", "Code"),)


class Content(models.Model):
    class Meta:
        ordering = ("sequence", )

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

        if first_content_created is True:
            self.sequence = 0

        actual_contents = self.post.content_set.order_by("sequence")
        contents_count = actual_contents.count()

        print(f"Jo: {self.sequence} - {contents_count}")

        if content_created is True:
            if contents_count > 0 and self.sequence is None:
                self.sequence = actual_contents.last().sequence + 1
        else:
            if contents_count > 0 and self.sequence is not None and self.sequence < contents_count:
                actual_contents.filter(sequence__gte=self.sequence).update(sequence=F("sequence") + 1)

        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

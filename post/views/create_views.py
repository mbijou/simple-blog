from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from content.views.management.manage_image_form import save_image_form
from post.forms import PostForm
from content.forms import ContentNewForm, ImageForm
from post.models import Post, LanguageGroup
from django.db import transaction
from django.utils import translation


class PostCreateView(LoginRequiredMixin, View):
    form = None
    content_form = None
    image_form = None

    def get(self, request, title=None):
        context = self.get_context(request)

        post_to_be_translated = context.get("post_to_be_translated")

        translation_already_existing_page = self.check_if_translation_exists(post_to_be_translated, request, context)

        if translation_already_existing_page:
            return translation_already_existing_page

        return self.get_render(request, context)

    @transaction.atomic
    def post(self, request, title=None):
        context = self.get_context(request)

        post_to_be_translated = context.get("post_to_be_translated")

        translation_already_existing_page = self.check_if_translation_exists(post_to_be_translated, request, context)

        if translation_already_existing_page:
            return translation_already_existing_page

        error_page = self.get_render(request, context)

        if self.form.is_valid() is True and self.content_form.is_valid() is True:
            new_post_instance = self.form.save()
            content_instance = self.content_form.save(post=new_post_instance)

            save_image_form(content_instance, self.image_form, transaction)

            self.marry_multi_language_posts(new_post_instance, post_to_be_translated)

            if transaction.get_rollback() is True:
                return error_page

            return HttpResponseRedirect(
                reverse_lazy("blog:post-detail", kwargs={"title": new_post_instance.title_slugified()}))
        else:
            return error_page

    def get_context(self, request):
        self.form = self.get_form(request, PostForm)
        self.content_form = self.get_form(request, ContentNewForm)
        self.image_form = self.get_form(request, ImageForm)
        post_to_be_translated_title = self.kwargs.get("title")
        post_to_be_translated = self.get_post_to_be_translated(post_to_be_translated_title)
        context = {"form": self.form, "content_form": self.content_form, "image_form": self.image_form,
                   "post_to_be_translated_title": post_to_be_translated_title,
                   "post_to_be_translated": post_to_be_translated}
        return context

    def marry_multi_language_posts(self, new_post: Post, post_to_be_translated):
        if post_to_be_translated:
            language_group = self.get_language_group(post_to_be_translated)
            new_post.language_group = language_group
            new_post.save()
            post_to_be_translated.language_group = language_group
            post_to_be_translated.save()

    @staticmethod
    def check_if_translation_exists(post_to_be_translated: Post, request, context):
        if post_to_be_translated:
            if post_to_be_translated.language_group is not None:
                try:
                    existing_post = Post.objects_from_all_languages.get(
                        language_group=post_to_be_translated.language_group, language_code=translation.get_language())
                    context["existing_post"] = existing_post
                    return render(request, template_name="post/new/error_translate.html", context=context)
                except Post.DoesNotExist:
                    pass
            if post_to_be_translated.language_code == translation.get_language():
                context["existing_post"] = post_to_be_translated
                return render(request, template_name="post/new/error_translate.html", context=context)

    @staticmethod
    def get_language_group(post_to_be_translated):
        language_group = post_to_be_translated.language_group

        if not language_group:
            language_group = LanguageGroup.objects.create()

        return language_group

    @staticmethod
    def get_post_to_be_translated(title):
        if title is None:
            return

        try:
            post_to_be_translated = Post.objects_from_all_languages.get(slug_title=title)
            return post_to_be_translated
        except Post.DoesNotExist:
            raise Http404('No %s matches the given query.' % Post._meta.object_name)

    @staticmethod
    def get_post_language(post: Post):
        if post is not None:
            return post.language_code

    @staticmethod
    def get_post_image(post: Post):
        return post.post_image

    @staticmethod
    def get_form(request, form_class):
        print(f"??? {request.FILES} {request.POST}")
        if request.POST and request.FILES:
            form = form_class(request.POST, files=request.FILES)
            print("yeah")
        elif request.POST:
            form = form_class(request.POST)
        else:
            form = form_class()
        return form

    def get_render(self, request, context):
        return render(request, template_name="post/new.html", context=context)

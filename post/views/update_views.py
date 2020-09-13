from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from blog.views.detail_views import get_redirect_to_other_language, get_post_from_all_languages
from post.forms import PostForm
from content.forms import ContentNewForm, ImageForm
from post.models import Post
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils import translation


class PostUpdateView(LoginRequiredMixin, View):
    form = None
    content_form = None
    image_form = None
    instance = None

    def get(self, request, title=None):
        context = self.get_context(request)

        instance = context.get("object")
        language_group = instance.language_group

        if instance.language_code != translation.get_language():
            redirect_to_other_language = get_redirect_to_other_language(language_group)

            if redirect_to_other_language:
                return redirect_to_other_language

            context["object"] = None
        return self.get_render(request, context)

    @atomic
    def post(self, request, title=None):
        context = self.get_context(request)
        error_page = self.get_render(request, context)

        if self.form.is_valid() is True:
            instance = self.form.save()
            return HttpResponseRedirect(reverse_lazy("post:edit", kwargs={"title": instance.slug_title}))
        else:
            return error_page

    def get_context(self, request):
        title = self.kwargs.get("title")
        self.instance = self.get_instance(title)

        post_language = self.get_post_language(self.instance)
        post_image = self.get_post_image(self.instance)

        self.form = self.get_form(request, PostForm)
        self.content_form = self.get_form(request, ContentNewForm)
        self.image_form = self.get_form(request, ImageForm)
        context = {"form": self.form, "content_form": self.content_form, "image_form": self.image_form,
                   "object": self.instance, "post_language": post_language, "post_image": post_image,
                   "title": title}
        return context

    def get_form(self, request, form_class):
        if self.request.POST and request.FILES:
            form = form_class(request.POST, files=request.FILES, instance=self.instance)
        elif self.request.POST:
            form = form_class(request.POST, instance=self.instance)
        else:
            form = form_class(instance=self.instance)
        return form

    def get_render(self, request, context):
        print("!!!")
        return render(request, template_name="post/edit.html", context=context)

    def get_instance(self, title):
        return get_post_from_all_languages(title)

    @staticmethod
    def get_post_language(post: Post):
        if post is not None:
            return post.language_code

    @staticmethod
    def get_post_image(post: Post):
        return post.post_image

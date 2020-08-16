from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from content.views.management.manage_image_form import save_image_form
from post.forms import PostForm
from content.forms import ContentForm, ImageForm
from post.models import Post
from django.db import transaction


class PostCreateView(LoginRequiredMixin, View):
    form = None
    content_form = None
    image_form = None

    def get(self, request):
        return self.get_render(request)

    @transaction.atomic
    def post(self, request):
        error_page = self.get_render(request)

        if self.form.is_valid() is True and self.content_form.is_valid() is True:
            post_instance = self.form.save()
            content_instance = self.content_form.save(post=post_instance)

            save_image_form(content_instance, self.image_form, transaction)

            if transaction.get_rollback() is True:
                return error_page

            return HttpResponseRedirect(reverse_lazy("blog:post-detail", kwargs={"title": post_instance.title_slugified()}))
        else:
            return error_page

    def get_context(self, request):
        self.form = self.get_form(request, PostForm)
        self.content_form = self.get_form(request, ContentForm)
        self.image_form = self.get_form(request, ImageForm)
        context = {"form": self.form, "posts": self.get_posts(), "content_form": self.content_form,
                   "image_form": self.image_form}
        return context

    def get_form(self, request, form_class):
        if request.POST and request.FILES:
            form = form_class(request.POST, files=request.FILES)
        elif request.POST:
            form = form_class(request.POST)
        else:
            form = form_class()
        return form

    def get_posts(self):
        return Post.objects.all()

    def get_render(self, request):
        return render(request, template_name="post/new.html", context=self.get_context(request))

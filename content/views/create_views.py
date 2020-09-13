from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from content.views.management.manage_image_form import save_image_form
from post.forms import PostForm
from content.forms import ContentNewForm, ImageForm
# Create your views here.
from post.models import Post
from django.db import transaction
from django.shortcuts import get_object_or_404


class ContentCreateView(LoginRequiredMixin, View):
    post_form = None
    content_form = None
    image_form = None

    post_instance = None
    content_instance = None

    @transaction.atomic
    def post(self, request, title=None):
        error_page = self.get_render(request)

        if self.content_form.is_valid() is True:
            self.content_instance = self.content_form.save(post=self.post_instance)

            save_image_form(self.content_instance, self.image_form, transaction)

            if transaction.get_rollback() is True:
                return error_page

            return HttpResponseRedirect(reverse_lazy("post:edit", kwargs={"title": self.post_instance.slug_title}))
        else:
            return error_page

    def get_context(self, request):
        self.post_instance = get_object_or_404(Post.objects_from_local_language, slug_title=self.kwargs.get("title"))
        self.post_form = PostForm(instance=self.post_instance)
        self.image_form = self.get_form(request, ImageForm, None)
        self.content_form = self.get_form(request, ContentNewForm, None)
        context = {"post_form": self.post_form, "content_form": self.content_form,
                   "image_form": self.image_form, "post_instance": self.post_instance}
        return context

    def get_form(self, request, form_class, instance):
        if self.request.POST and self.request.FILES:
            form = form_class(request.POST, files=self.request.FILES, instance=instance)
        elif self.request.POST:
            form = form_class(request.POST, instance=instance)
        else:
            form = form_class(instance=instance)
        return form

    def get_render(self, request):
        return render(request, template_name="content/new.html", context=self.get_context(request))

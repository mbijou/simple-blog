from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from content.views.management.manage_image_form import save_image_form
from post.forms import PostForm
from content.forms import ContentUpdateForm, ImageForm
from post.models import Post, Content
from django.db import transaction
from django.shortcuts import get_object_or_404


class ContentUpdateView(LoginRequiredMixin, View):
    post_form = None
    content_form = None
    image_form = None

    post_instance = None
    content_instance = None
    image_instance = None

    def get(self, request, title=None, content_pk=None):
        return self.get_render(request)

    @transaction.atomic
    def post(self, request, title=None, content_pk=None):
        error_page = self.get_render(request)

        if self.content_form.is_valid() is True:
            self.content_instance = self.content_form.save()

            save_image_form(self.content_instance, self.image_form, transaction)

            if transaction.get_rollback() is True:
                return error_page

            # last_url used for next page for javascript to scroll to the a tag that has that last_url
            last_url = str(reverse_lazy("content:edit",
                                        kwargs={"title": self.post_instance.slug_title,
                                                "content_pk": self.content_instance.pk}))

            return HttpResponseRedirect(
                reverse_lazy("post:edit", kwargs={"title": self.post_instance.slug_title}) + f"?last=" + last_url)
        else:
            return error_page

    def get_context(self, request):
        self.post_instance = get_object_or_404(Post.objects_from_local_language, slug_title=self.kwargs.get("title"))
        self.content_instance = self.get_instance(Content, self.kwargs.get("content_pk"))
        if self.content_instance:
            self.image_instance = self.content_instance.get_image()
            print(self.image_instance)

        self.post_form = PostForm(instance=self.post_instance)
        self.content_form = self.get_form(request, ContentUpdateForm, instance=self.content_instance)
        self.image_form = self.get_form(request, ImageForm, instance=self.image_instance)
        context = {"post_form": self.post_form, "content_form": self.content_form, "post_instance": self.post_instance,
                   "image_form": self.image_form, "content_pk": self.kwargs.get("content_pk")}
        return context

    def get_form(self, request, form_class, instance):
        if request.POST and request.FILES:
            form = form_class(request.POST, files=request.FILES, instance=instance)
        elif request.POST:
            form = form_class(request.POST, instance=instance)
        else:
            form = form_class(instance=instance)
        return form

    def get_render(self, request):
        return render(request, template_name="content/edit.html", context=self.get_context(request))

    def get_instance(self, instance_class, pk):
        return get_object_or_404(instance_class, pk=pk)

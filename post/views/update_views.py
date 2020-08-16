from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from post.forms import PostForm
from content.forms import ContentForm, ImageForm
from post.models import Post
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404


class PostUpdateView(LoginRequiredMixin, View):
    form = None
    content_form = None
    image_form = None
    instance = None

    def get(self, request, pk=None):
        return self.get_render(request)

    @atomic
    def post(self, request, pk=None):
        error_page = self.get_render(request)

        if self.form.is_valid() is True:
            self.form.save()
            return HttpResponseRedirect(reverse_lazy("post:edit", kwargs={"pk": self.kwargs.get("pk")}))
        else:
            return error_page

    def get_context(self, request):
        self.instance = self.get_instance(Post)
        self.form = self.get_form(request, PostForm)
        self.content_form = self.get_form(request, ContentForm)
        self.image_form = self.get_form(request, ImageForm)
        context = {"form": self.form, "content_form": self.content_form, "image_form": self.image_form,
                   "object": self.instance}
        return context

    def get_form(self, request, form_class):
        if self.request.POST and request.FILES:
            form = form_class(request.POST, files=request.FILES, instance=self.instance)
        elif self.request.POST:
            form = form_class(request.POST, instance=self.instance)
        else:
            form = form_class(instance=self.instance)
        return form

    def get_render(self, request):
        print("!!!")
        return render(request, template_name="post/edit.html", context=self.get_context(request))

    def get_instance(self, instance_class):
        return get_object_or_404(instance_class, pk=self.kwargs.get("pk"))

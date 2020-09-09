from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post


class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, title=None):
        self.delete(title)
        return HttpResponseRedirect(reverse_lazy("post:new"))

    def delete(self, title):
        instance = get_object_or_404(Post.objects_from_local_language, slug_title=title)
        instance.delete()

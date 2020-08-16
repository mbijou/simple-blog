from django.shortcuts import render, get_object_or_404
from django.views import View
from post.models import Post
from django.utils.text import slugify


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "blog/detail.html", {"post": self.get_instance()})

    def get_instance(self):
        if self.kwargs.get("pk"):
            return get_object_or_404(Post, pk=self.kwargs.get("pk"))
        elif self.kwargs.get("title"):
            return get_object_or_404(Post, slug_title=self.kwargs.get("title"))

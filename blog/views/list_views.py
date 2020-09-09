from django.shortcuts import render
from django.views import View
from post.models import Post


class PostListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "blog/blog.html", {"posts": Post.objects_from_local_language.all()})

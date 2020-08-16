from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post


class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk=None):
        self.delete(pk)
        return HttpResponseRedirect(reverse_lazy("post:new"))

    def delete(self, pk):
        instance = get_object_or_404(Post, pk=pk)
        instance.delete()

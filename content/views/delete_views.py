from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db.transaction import atomic
from django.db.models import F
from post.models import Content
from django.contrib.auth.mixins import LoginRequiredMixin


class ContentDeleteView(LoginRequiredMixin, View):
    @atomic
    def post(self, request, title=None, content_pk=None):
        self.delete(content_pk, title)
        return HttpResponseRedirect(reverse_lazy("post:edit", kwargs={"title": title}))

    def delete(self, content_pk, post_title):
        instance = get_object_or_404(Content, pk=content_pk)
        sequence = instance.sequence
        contents_of_higher_sequence = Content.objects.filter(post__slug_title=post_title, sequence__gt=sequence)
        instance.delete()
        contents_of_higher_sequence.update(sequence=F("sequence")-1)

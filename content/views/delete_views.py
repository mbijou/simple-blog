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
    def post(self, request, pk=None, content_pk=None):
        self.delete(content_pk, pk)
        return HttpResponseRedirect(reverse_lazy("post:edit", kwargs={"pk": pk}))

    def delete(self, content_pk, post_pk):
        instance = get_object_or_404(Content, pk=content_pk)
        sequence = instance.sequence
        contents_of_higher_sequence = Content.objects.filter(post__pk=post_pk, sequence__gt=sequence)
        instance.delete()
        contents_of_higher_sequence.update(sequence=F("sequence")-1)
